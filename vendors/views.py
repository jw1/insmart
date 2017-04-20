from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from vendors.models import Vendor


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'website_address', 'contact_name', 'contact_email', 'contact_phone', 'physical_address_line_1', 'physical_address_line_2', 'physical_address_city', 'physical_address_state', 'physical_address_postal_code', 'physical_address_country', 'mailing_address_line_1', 'mailing_address_line_2', 'mailing_address_state', 'mailing_address_postal_code',
'mailing_address_country', 'active']

def vendor_list(request, template_name='vendors/vendor_list.html'):
    vendors = Vendor.objects.all()
    data = {}
    data['object_list'] = vendors
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
