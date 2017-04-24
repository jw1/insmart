from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from alert.models import Alert
from django.views.generic import DetailView
from insmart_core.search import get_query

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['product', 'minimum', 'maximum', 'current']
        search_fields = ['minimum', 'maximum', 'current']

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