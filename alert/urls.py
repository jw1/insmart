from django.conf.urls import url
from alert import views

urlpatterns = [
    url(r'^$',
        views.alert_list,
        name='alert_list'),

    url(r'^detail/(?P<pk>\d+)$',
        views.AlertDetail.as_view(),
        name='alert_detail')
    ]
