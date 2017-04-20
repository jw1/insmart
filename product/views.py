from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['vendors', 'name', 'description', 'brand',
              'minimum', 'maximum', 'current', 'active']

def product_list(request, template_name = 'product/product_list.html'):
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

def product_update(request, pk, template_name='product/product_form.html'):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance = product)
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