from django.db import models
from django.core.urlresolvers import reverse
from vendors.models import Vendor
# Create your models here.

class Product(models.Model):
    vendors = models.ManyToManyField(Vendor)
    name = models.CharField(max_length=50)
    description = models.CharField(null=True, max_length=250)
    brand = models.CharField(null=True, max_length=50)
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=9999999)
    current = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_edit', kwargs={'pk': self.pk})

    #Deletes should only make an object inactive so as not to break inventory opns.
    def delete(self, using=None, keep_parents=False):
        self.active = False
        self.save()
        return self
