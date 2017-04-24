from django.conf.urls import url
from product import views

urlpatterns = [
    url(r'^$',
        views.product_list,
        name='product_list'),

    url(r'^new$',
        views.product_create,
        name='product_new'),

    url(r'^edit/(?P<pk>\d+)$',
        views.product_update,
        name='product_edit'),

    url(r'^delete/(?P<pk>\d+)$',
        views.product_delete,
        name='product_delete'),

    url(r'^detail/(?P<pk>\d+)$',
        views.ProductDetail.as_view(),
        name='product_detail'),

    url(r'^list_all$',
        views.product_list_all,
        name='product_list_all'),
    ]
