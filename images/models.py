from __future__ import unicode_literals

from django.db import models
from accounts.models import BlitzUser

from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.

class Topic(models.Model):
    name        = models.CharField(max_length=64)
    startDate   = models.DateTimeField(default=django.utils.timezone.now)
    endDate     = models.DateTimeField(default=django.utilz.timezone.now+datetime.timedelta(days=365))

    def __str__(self):
        return self.name

class Chapter(models.Model):
    name        = models.CharField(max_length=64)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE)

class UserTopic(models.Model):
    user        = models.ForeignKey(BlitzUser, on_delete=models.CASCADE)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE)
    likes       = models.IntegerField(default=0)
    dislikes    = models.IntegerField(default=0)
    likedBy     = models.ManyToManyField(BlitzUser, related_name='likes')
    dislikedBy  = models.ManyToManyField(BlitzUser, related_name='dislikes')


def user_directory_path(instance, filename):
    username                = instance.userTopic.user.user.username
    topicId                 = instance.userTopic.id
    chapterId               = instance.id
    return '{0}/topic/{1}/chapter/{2}/{3}'.format(username, topicId, chapterId, filename)



class UserChapter(models.Model):
    image               = models.ImageField(upload_to=user_directory_path)
    userTopic           = models.ForeignKey(UserTopic, on_delete=models.CASCADE)
    chapter             = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.chapter.name

class Blitz(models.Model):
    user1               = models.ForeignKey(BlitzUser, related_name='blitzUser1', on_delete=models.CASCADE)
    user2               = models.ForeignKey(BlitzUser, related_name='blitzUser2', on_delete=models.CASCADE)
    winner              = models.ForeignKey(BlitzUser, related_name='wins', on_delete=models.CASCADE)
    userTopic           = models.ForeignKey(UserTopic, on_delete=models.CASCADE)

    def __str__(self):
        return self.user1 + ", " + self.user2

