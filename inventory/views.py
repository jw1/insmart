from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import AuditLog
from product.models import Product
from alert.models import Alert
from django.views.generic import DetailView

class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ['product', 'user_id', 'before', 'after', 'adjustment', 'memo']
        exclude = ['before', 'after']
        search_fields = ['memo']

class UpdateAuditLogForm(AuditLogForm):
    current = forms.CharField(disabled=True)

class AuditLogDetail(DetailView):
    queryset = AuditLog.objects.all()
    def get_object(self):
        object = super(AuditLogDetail, self).get_object()
        return object

def audit_log_list(request, template_name = 'inventory/auditlog_list.html'):

    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, AuditLogForm.Meta.search_fields)
        result_set = AuditLog.objects.filter(entry_query)
    else:
        result_set = AuditLog.objects.all()
    data = {}
    data['object_list'] = result_set
    return render(request, template_name, data)

def audit_log_create(request, template_name = 'inventory/auditlog_form.html'):
    form = AuditLogForm(request.POST or None)

    if form.is_valid():
        # 2-step save.  Can't commit until the calculated fields are set.
        form_to_save = form.save(commit=False)
        product = form.cleaned_data['product']
        current = product.current
        adjustment = form.cleaned_data['adjustment']
        form_to_save.before = current
        form_to_save.after = current + adjustment
        form_to_save.save()

        # go adjust the inventory level on the product
        adjust_product_inventory(product.id, current + adjustment)

        # did that inventory adjustment trigger an alert?
        if (is_alert_needed(product, form_to_save)):
            generate_alert(product, form_to_save)

        return redirect('audit_log_list')

    return render(request, template_name, {'form':form})

def adjust_product_inventory(product_id, new_count):
    product = Product.objects.filter(id = product_id).first()
    product.current = new_count
    Product.save(product)


def is_alert_needed(product, audit_log):

    if (audit_log.before > product.minimum and audit_log.after < product.minimum):
        return True

    if (audit_log.before < product.maximum and audit_log.after > product.maximum):
        return True

    return False

def generate_alert(product, audit_log):
    alert = Alert()
    alert.product = product
    alert.audit_log = audit_log
    alert.minimum = product.minimum
    alert.maximum = product.maximum
    alert.current = audit_log.after
    alert.save()

def audit_log_update(request, pk, template_name='inventory/auditlog_form.html'):
    audit_log = get_object_or_404(AuditLog, pk=pk)
    form = UpdateAuditLogForm(request.POST or None, instance = audit_log)
    if form.is_valid():
        form.save()
        return redirect('audit_log_list')
    return render(request, template_name, {'form':form})





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