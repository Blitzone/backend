from rest_framework import serializers
from .models import BlitzUser

class BlitzUserSerializer(serializers.ModelSerializer):
    user   = serializers.CharField(source='user.username')
    avatar = serializers.ImageField(max_length=None)
    class Meta:
        model = BlitzUser
        fields = ('user', 'avatar', 'blitzCount', 'is_banned')

class SearchBlitzUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.requestingUser = kwargs.pop('requestingUser', None)
        super(SearchBlitzUserSerializer, self).__init__(*args, **kwargs)

    user = serializers.CharField(source='user.username')
    isFollowed = serializers.SerializerMethodField('isFollowed')

    def isFollowed(self, user):
        requestingBlitzUser = BlitzUser.objects.get(user__username=self.requestingUser)
        return True

    class Meta:
        model = BlitzUser
        fields = ('user', 'isFollowed')