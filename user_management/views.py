from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User

class UserList(ListView):
    model = User

class UserCreate(CreateView):
    model = User
    success_url = reverse_lazy('user_list')
    fields = ['email', 'first_name', 'last_name', 'is_superuser', 'is_active']

class UserUpdate(UpdateView):
    model = User
    success_url = reverse_lazy('user_list')
    fields = ['email', 'first_name', 'last_name', 'is_superuser', 'is_active']

class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')