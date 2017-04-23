from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from alert.models import Alert
from product.models import Product
from inventory.models import AuditLog
from django.views.generic import DetailView

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['product', 'minimum', 'maximum', 'current']
        search_fields = ['product']

class AlertDetail(DetailView):
    queryset = Alert.objects.all()
    def get_object(self):
        object = super(AlertDetail, self).get_object()
        return object

def alert_list(request, template_name = 'alert/alert_list.html'):

    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, AlertForm.Meta.search_fields)
        result_set = Alert.objects.filter(entry_query)
    else:
        result_set = Alert.objects.all()
    data = {}
    data['object_list'] = result_set
    return render(request, template_name, data)


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