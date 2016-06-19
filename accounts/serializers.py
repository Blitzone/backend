from rest_framework import serializers
from .models import BlitzUser

class BlitzUserSerializer(serializers.ModelSerializer):
    user   = serializers.CharField(source='user.username')
    avatar = serializers.ImageField(max_length=None)
    followers = serializers.SerializerMethodField('getNumFollowers')

    def getNumFollowers(self, user):
        return BlitzUser.objects.filter(follows=user).len()
    class Meta:
        model = BlitzUser
        fields = ('user', 'avatar', 'blitzCount', 'followers', 'is_banned')

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
        fields = ('user', 'avatar', 'blitzCount', 'is_banned', 'is_followed')

# class ProfileBlitzUserSerializer(serializers.ModelSerializer):
#     user   = serializers.CharField(source='user.username')
#     avatar = serializers.ImageField(max_length=None)
#     followers = serializers.SerializerMethodField('getFollowers')
#     following = serializers.SerializerMethodField('getFollowing')
#
#     def getFollowing(self, user):
#         return BlitzUserSerializer(user.follows.all(), many=True).data
#     def getFollowers(self, user):
#         return BlitzUserSerializer(BlitzUser.objects.filter(follows=user), many=True).data
#     class Meta:
#         model = BlitzUser
#         fields = ('user', 'avatar', 'blitzCount', 'is_banned', 'followers', 'following')
