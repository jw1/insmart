from django.contrib import admin
from .models import Question, Product


# Register your models here.
admin.site.register(Question)
admin.site.register(Product)