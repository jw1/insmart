from django.conf.urls import url

from user_management import views

urlpatterns = [
  url(r'^$', views.UserList.as_view(), name='user_list'),
  url(r'^new$', views.UserCreate.as_view(), name='user_new'),
  url(r'^edit/(?P<pk>\d+)$', views.UserUpdate.as_view(), name='user_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.UserDelete.as_view(), name='user_delete'),
]
