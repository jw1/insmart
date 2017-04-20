from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from vendors.models import Vendor
from django.views.generic import DetailView

class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'website_address', 'contact_name', 'contact_email', 'contact_phone', 'physical_address_line_1', 'physical_address_line_2', 'physical_address_city', 'physical_address_state', 'physical_address_postal_code', 'physical_address_country', 'mailing_address_line_1', 'mailing_address_line_2', 'mailing_address_state', 'mailing_address_postal_code',
'mailing_address_country', 'active']

def vendor_list(request, template_name='vendors/vendor_list.html'):

    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, VendorForm.Meta.fields) # I search on all fields.  Adjust as needed.
        vendor = Vendor.objects.filter(entry_query)
    else:
        vendor = Vendor.objects.all()

    data = {}
    data['object_list'] = vendor
    return render(request, template_name, data)

def vendor_create(request, template_name='vendors/vendors_form.html'):
    form = VendorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vendor_list')
    return render(request, template_name, {'form':form})

def vendor_update(request, pk, template_name='vendors/vendors_form.html'):
    vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(request.POST or None, instance=vendor)
    if form.is_valid():
        form.save()
        return redirect('vendor_list')
    return render(request, template_name, {'form':form})

def vendor_delete(request, pk, template_name='vendors/vendor_confirm_delete.html'):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method=='POST':
        vendor.delete()
        return redirect('vendor_list')
    return render(request, template_name, {'object':vendor})

class VendorDetail(DetailView):
    queryset = Vendor.objects.all()
    def get_object(self):
        object = super(VendorDetail, self).get_object()
        return object


import re
from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):

    ''' Returns a query, that is a combination of Q objects. That combination aims to search keywords within a model by testing the given search fields. '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query