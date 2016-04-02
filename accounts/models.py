from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlitzUser(models.Model):
    user        = models.OneToOneField(User)
    avatar      = models.CharField(max_length=64)
    blitzCount  = models.IntegerField(default=0)
    is_banned   = models.BooleanField(default=False)

    def natural_key(self):
        return self.user.natural_key()
    natural_key.dependencies = ['django.contrib.auth.models.User']
    def __str__(self):
        return self.user.username