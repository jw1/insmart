from django.db import models
from django.core.urlresolvers import reverse
from product.models import Product
from inventory.models import AuditLog

class Alert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    audit_log = models.ForeignKey(AuditLog, on_delete=models.CASCADE)
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=9999999)
    current = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.product + ' ' + self.audit_log + ' ' + str(self.created_at)

    def get_absolute_url(self):
        return reverse('alert_edit', kwargs={'pk': self.pk})