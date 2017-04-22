from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import AuditLog
from product.models import Product
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

        current = form.cleaned_data['product'].current
        adjustment = form.cleaned_data['adjustment']

        form_to_save.before = current
        form_to_save.after = current + adjustment

        form_to_save.save()

        # TODO:  if the adjustment was made, then see if alert needs to be made.

        return redirect('audit_log_list')

    return render(request, template_name, {'form':form})

def clean_before(self):
    current = self.cleaned_data['product'].current
    print(current)
    #adjustment = self.cleaned_data['adjustment']
    #print('vals')
    #print(current)
    #print(adjustment)

    #form.before = current
    #form.after = current + adjustment

    #form.cleaned_data['before'] = current
    #form.cleaned_data['after'] = current + adjustment
    return current

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