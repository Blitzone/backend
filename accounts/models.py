from __future__ import unicode_literals

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)

# Create your models here.
class BlitzUser(models.Model):
    user        = models.OneToOneField(User)
    avatar      = models.ImageField(upload_to=user_directory_path)
    blitzCount  = models.IntegerField(default=0)
    is_banned   = models.BooleanField(default=False)
    follows     = models.ManyToManyField('BlitzUser', related_name='followed_by')

    def natural_key(self):
        return self.user.natural_key()
    natural_key.dependencies = ['django.contrib.auth.models.User']
    def __str__(self):
        return self.user.username


class Notification(models.Model):
    text        = models.CharField(max_length=128)
    link        = models.CharField(max_length=256)
    user        = models.ForeignKey(BlitzUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.text