from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from product.models import Product

# when we adjust inventory
class AuditLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    before = models.IntegerField()
    after = models.IntegerField()
    adjustment = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    memo = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('audit_log_edit', kwargs={'pk': self.pk})