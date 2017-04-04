from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from product.models import Product

class ProductList(ListView):
    model = Product

class ProductCreate(CreateView):
    model = Product
    success_url = reverse_lazy('product_list')
    fields = ['vendors', 'name', 'description', 'brand',
              'minimum', 'maximum', 'current' ]

class ProductUpdate(UpdateView):
    model = Product
    success_url = reverse_lazy('product_list')

class ProductDelete(DeleteView):
    model = Product
    success_url = ('product_list')
