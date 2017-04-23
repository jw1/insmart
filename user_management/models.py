from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Note:  we're using the built-in User model.

# I guess that means receives alerts.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = active = models.BooleanField(default=False)
