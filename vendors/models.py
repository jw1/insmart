from django.db import models
from django.core.urlresolvers import reverse
#from polls.models import Vendor
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(default=" ", max_length=100)
    website_address = models.CharField(default="", max_length=200)
    contact_name = models.CharField(default="", max_length=100)
    contact_email = models.CharField(default="", max_length=100)
    contact_phone = models.CharField(default="", max_length=100)
    physical_address_line_1 = models.CharField(default="", max_length=100)
    physical_address_line_2 = models.CharField(default="", max_length=100)
    physical_address_city = models.CharField(default="", max_length=100)
    physical_address_state = models.CharField(default="", max_length=50)
    physical_address_postal_code = models.CharField(default="", max_length=25)
    physical_address_country = models.CharField(default="", max_length=50)
    mailing_address_line_1 = models.CharField(default="", max_length=100)
    mailing_address_line_2 = models.CharField(default="", max_length=100)
    mailing_address_state = models.CharField(default="", max_length=50)
    mailing_address_postal_code = models.CharField(default="", max_length=25)
    mailing_address_country = models.CharField(default="", max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor_edit', kwargs={'pk': self.pk})