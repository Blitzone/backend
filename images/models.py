from __future__ import unicode_literals

from django.db import models
from accounts.models import BlitzUser
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.

class Topic(models.Model):
    name        = models.CharField(max_length=64)
    startDate   = models.DateTimeField(default=0)
    endDate     = models.DateTimeField(default=0)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    name        = models.CharField(max_length=64)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name


class UserTopic(models.Model):
    user        = models.ForeignKey(BlitzUser, on_delete=models.CASCADE, default=0)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE, default=0)
    likes       = models.IntegerField(default=0)
    dislikes    = models.IntegerField(default=0)
    likedBy     = models.ManyToManyField(BlitzUser, related_name='likes')
    dislikedBy  = models.ManyToManyField(BlitzUser, related_name='dislikes')

    def __str__(self):
        return self.topic.name



def user_directory_path(instance, filename):
    username                = instance.userTopic.user.user.username
    topicId                 = instance.userTopic.id
    chapterId               = instance.id
    return '{0}/topic/{1}/chapter/{2}/{3}'.format(username, topicId, chapterId, filename)



class UserChapter(models.Model):
    image               = models.ImageField(upload_to=user_directory_path)
    userTopic           = models.ForeignKey(UserTopic, on_delete=models.CASCADE, default=0)
    chapter             = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.chapter.name

class Blitz(models.Model):
    user1               = models.ForeignKey(BlitzUser, related_name='blitzUser1', on_delete=models.CASCADE, default=0)
    user2               = models.ForeignKey(BlitzUser, related_name='blitzUser2', on_delete=models.CASCADE, default=0)
    winner              = models.ForeignKey(BlitzUser, related_name='wins', on_delete=models.CASCADE, default=0)
    userTopic           = models.ForeignKey(UserTopic, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.user1 + ", " + self.user2

