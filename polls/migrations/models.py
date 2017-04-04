from __future__ import unicode_literals
from django.db import models

# Create your models here.
# Models from Tutorial here


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

# Models for InSmart
class Vendor(models.Model):
    name = models.CharField(max_length=100)
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

class InventoryAuditLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    before = models.IntegerField()
    after = models.IntegerField()
    adjustment = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    memo = models.TextField(null=True)



