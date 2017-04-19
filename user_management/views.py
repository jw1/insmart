from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_active']


def user_list(request, template_name='user_management/user_list.html'):

    # search if something was provided to search on
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, UserForm.Meta.fields) # I search on all fields.  Adjust as needed.
        users = User.objects.filter(entry_query)
    else:
        users = User.objects.all()

    data = {}
    data['object_list'] = users
    return render(request, template_name, data)

def user_create(request, template_name='user_management/user_form.html'):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, template_name, {'form':form})

def user_update(request, pk, template_name='user_management/user_form.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, template_name, {'form':form})

def user_delete(request, pk, template_name='user_management/user_confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('user_list')
    return render(request, template_name, {'object':user})



# quick and dirty search impl here
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