from django.db import models
from django.core.urlresolvers import reverse
from polls.models import Product
# Create your models here.

class Product(models.Model):
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_edit', kwargs={'pk': self.pk})


