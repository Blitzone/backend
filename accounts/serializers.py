from rest_framework import serializers
from .models import BlitzUser

class BlitzUserSerializer(serializers.ModelSerializer):
    user   = serializers.CharField(source='user.username')
    avatar = serializers.ImageField(max_length=None)
    class Meta:
        model = BlitzUser
        fields = ('user', 'avatar', 'blitzCount', 'is_banned')