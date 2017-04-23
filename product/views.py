from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from django.views.generic import DetailView
from insmart_core.search import get_query
from inventory.models import AuditLog
from alert.models import Alert

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendors', 'name', 'description', 'brand',
              'minimum', 'maximum', 'current', 'active']
        search_fields = ['name', 'description', 'brand',
              'minimum', 'maximum', 'current', 'active']

class UpdateProductForm(ProductForm):
    current = forms.CharField(disabled=True)

class ProductDetail(DetailView):
    queryset = Product.objects.all()
    def get_object(self):
        object = super(ProductDetail, self).get_object()
        return object


def product_list(request, template_name = 'product/product_list.html'):
    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ProductForm.Meta.search_fields) # I search all product fields.  Adjust as needed.
        product = Product.objects.filter(entry_query)
    else:
        product = Product.objects.all()
    data = {}
    data['object_list'] = product
    return render(request, template_name, data)

def product_create(request, template_name = 'product/product_form.html'):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, template_name, {'form':form})

def product_delete(request, pk, template_name='product/product_confirm_delete.html'):
    product = get_object_or_404(Product, pk=pk)
    if request.method=='POST':
        product.delete()
        return redirect('product_list')
    return render(request, template_name, {'object':product})

def product_update(request, pk, template_name='product/product_form.html'):
    product = get_object_or_404(Product, pk=pk)
    form = UpdateProductForm(request.POST or None, instance = product)
    if form.is_valid():

        # Note "pre-save" values so we can see if we generated an alert
        before_save_minimum = form.initial['minimum']
        before_save_maximum = form.initial['maximum']

        form.save()

        if (is_alert_needed(product, before_save_minimum, before_save_maximum)):
            generate_alert(product, request.user)

        return redirect('product_list')
    
    return render(request, template_name, {'form':form})

def is_alert_needed(product, before_save_minimum, before_save_maximum):
    ''' True if modification put current inventory level out of bounds, False otherwise. '''

    # before it was okay, after update we're under the limit
    if before_save_minimum <= product.current < product.minimum:
        return True

    # before it was okay, after update we're over the limit
    if before_save_maximum >= product.current > product.maximum:
        return True

    return False

def generate_alert(product, user):
    ''' Saves new audit_log and alert corresponding to the provided info '''

    # build an audit record to represent the product change
    audit = AuditLog()
    audit.product = product
    audit.user_id = user
    audit.before = product.current
    audit.after = product.current
    audit.adjustment = 0
    audit.memo = 'Auto-generated inventory adjustment -- product minimum and maximum changed.'
    audit.save()

    # and generate an alert associated with that audit record
    alert = Alert()
    alert.product = product
    alert.audit_log = audit
    alert.minimum = product.minimum
    alert.maximum = product.maximum
    alert.current = product.current
    alert.save()