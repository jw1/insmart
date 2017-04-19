from django.conf.urls import url

from user_management import views

urlpatterns = [
  url(r'^$', views.user_list, name='user_list'),
  url(r'^new$', views.user_create, name='user_new'),
  url(r'^edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
]
