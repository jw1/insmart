from django.conf.urls import url

from vendors import views

urlpatterns = [
  url(r'^$', views.vendor_list, name='vendor_list'),
  url(r'^new$', views.vendor_create, name='vendor_new'),
  url(r'^edit/(?P<pk>\d+)$', views.vendor_update, name='vendor_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.vendor_delete, name='vendor_delete'),
  url(r'^detail/(?P<pk>\d+)$', views.VendorDetail.as_view(), name='vendor_detail'),
]