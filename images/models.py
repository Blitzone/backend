from __future__ import unicode_literals

from django.db import models
from accounts.models import BlitzUser

# Create your models here.

class Image(models.Model):
    id          = models.BigIntegerField(default=0, primary_key=True)
    owner       = models.ForeignKey(BlitzUser, on_delete=models.CASCADE)
    path        = models.CharField(max_length=256)

    def __str__(self):
        return self.path

class Topic(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    user = models.ForeignKey(BlitzUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    likedBy = models.ManyToManyField(BlitzUser, related_name='likedBy')
    dislikedBy = models.ManyToManyField(BlitzUser, related_name='dislikedBy')

    def __str__(self):
        return self.name


class Chapter(models.Model):
    id          = models.IntegerField(default=0, primary_key=True)
    name        = models.CharField(max_length=64)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Blitz(models.Model):
    id          = models.IntegerField(default=0, primary_key=True)
    user1       = models.ForeignKey(BlitzUser, related_name='blitzUser1', on_delete=models.CASCADE)
    user2       = models.ForeignKey(BlitzUser, related_name='blitzUser2', on_delete=models.CASCADE)
    winner      = models.ForeignKey(BlitzUser, related_name='blitzWinner', on_delete=models.CASCADE)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE)
    startDate   = models.DateTimeField()

    def __str__(self):
        return self.user1 + ", " + self.user2

