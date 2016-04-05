from __future__ import unicode_literals

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlitzUser(models.Model):
    user        = models.OneToOneField(User)
    avatar      = models.ForeignKey('images.Image',default=1, on_delete=models.CASCADE)
    blitzCount  = models.IntegerField(default=0)
    is_banned   = models.BooleanField(default=False)

    def natural_key(self):
        return self.user.natural_key()
    natural_key.dependencies = ['django.contrib.auth.models.User']
    def __str__(self):
        return self.user.username


class Notification(models.Model):
    id          = models.BigIntegerField(default=0, primary_key=True)
    text        = models.CharField(max_length=128)
    link        = models.CharField(max_length=256)
    user        = models.ForeignKey(BlitzUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.text