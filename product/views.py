from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from django.views.generic import DetailView
from insmart_core.search import get_query
from insmart_core.mailer import send_alert_emails
from inventory.models import AuditLog
from alert.models import Alert
from django.db import transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['vendors', 'name', 'description', 'brand',
              'minimum', 'maximum', 'current', 'active']
        # search fields can't include m2m relationships-omitted vendors field
        search_fields = ['name', 'description', 'brand',
              'minimum', 'maximum', 'current', 'active']


    def clean(self):
        cleaned_data = self.cleaned_data
        vendor = cleaned_data.get('vendors')
        name = cleaned_data.get('name')
        brand = cleaned_data.get('brand')
        minimum = cleaned_data.get('minimum')
        maximum = cleaned_data.get('maximum')
        current = cleaned_data.get('current')
        # ensure no duplicates on vendors, name, and brands (different vendors maybe offer the same products)
        # but a vendor can't have two of the same product to sell.

        if Product.objects.filter(vendors = vendor, name = name, brand = brand).exclude(pk = self.instance.id).exists():
            del name
            del brand
            raise forms.ValidationError('This product is already defined for this vendor')

        if minimum > maximum:
            raise forms.ValidationError('Please either adjust your upper or lower limits')

        # had to convert current to int because it came as a string in this if argument
        # no clue why

        if minimum < 0 or maximum < 0 or int(current) < 0:
            del maximum
            del minimum
            raise  forms.ValidationError('Please use values between 0 and 2147483647')
        return cleaned_data

# This form disables current field adjustment to allow for management at inventory app
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
        product = Product.objects.filter(entry_query).filter(active=True).order_by('name')
    else:
        product = Product.objects.filter(active=True).order_by('name')
    data = {}
    data['object_list'] = product
    return render(request, template_name, data)

def product_list_all(request, template_name = 'product/product_list_all.html'):
    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ProductForm.Meta.search_fields) # I search all product fields.  Adjust as needed.
        product = Product.objects.filter(entry_query).order_by('name')
    else:
        product = Product.objects.all().order_by('name')
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
        #note deletes only set products to inactive state.
        product.delete()
        return redirect('product_list')
    return render(request, template_name, {'object':product})

@transaction.atomic
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

    # and notify as needed
    send_alert_emails(alert)