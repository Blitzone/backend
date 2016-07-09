from rest_framework import serializers
from .models import BlitzUser
from images.models import *

class BlitzUserSerializer(serializers.ModelSerializer):
    user   = serializers.CharField(source='user.username')
    avatar = serializers.ImageField(max_length=None)
    followers = serializers.SerializerMethodField('getNumFollowers')

    def getNumFollowers(self, user):
        return len(BlitzUser.objects.filter(follows=user))
    class Meta:
        model = BlitzUser
        fields = ('pk', 'user', 'avatar', 'blitzCount', 'followers', 'is_banned')

class SearchBlitzUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.requestingUser = kwargs.pop('requestingUser', None)
        super(SearchBlitzUserSerializer, self).__init__(*args, **kwargs)

    user = serializers.CharField(source='user.username')
    is_followed = serializers.SerializerMethodField('getIsFollowed')

    def getIsFollowed(self, user):
        requestingBlitzUser = BlitzUser.objects.get(user__username=self.requestingUser)
        return user in requestingBlitzUser.follows.all()

    class Meta:
        model = BlitzUser
        fields = ('pk', 'user', 'avatar', 'blitzCount', 'is_banned', 'is_followed')

class ProfileBlitzUserSerializer(serializers.ModelSerializer):
    user   = serializers.CharField(source='user.username')
    avatar = serializers.ImageField(max_length=None)
    followers = serializers.SerializerMethodField('getFollowers')
    likes = serializers.SerializerMethodField('getLikes')
    dislikes = serializers.SerializerMethodField('getDislikes')

    def getLikes(self, user):
        topic = Topic.objects.get(endDate__gt=datetime.datetime.now(), startDate__lte=datetime.datetime.now())
        userTopic = UserTopic.objects.get(user=user, topic=topic)
        return len(userTopic.likedBy.all())

    def getDislikes(self, user):
        topic = Topic.objects.get(endDate__gt=datetime.datetime.now(), startDate__lte=datetime.datetime.now())
        userTopic = UserTopic.objects.get(user=user, topic=topic)
        return len(userTopic.dislikedBy.all())

    def getFollowers(self, user):
        return len(BlitzUser.objects.filter(follows=user))
    class Meta:
        model = BlitzUser
        fields = ('user', 'avatar', 'blitzCount', 'is_banned', 'followers', 'likes', 'dislikes')
