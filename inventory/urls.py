from django.conf.urls import url
from inventory import views

urlpatterns = [
    url(r'^$',
        views.audit_log_list,
        name='audit_log_list'),

    url(r'^new$',
        views.audit_log_create,
        name='audit_log_new'),

    url(r'^detail/(?P<pk>\d+)$',
        views.AuditLogDetail.as_view(),
        name='audit_log_detail')
    ]
