from rest_framework import serializers
from .models import BlitzUser

class BlitzUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlitzUser
        fields = ('user', 'avatar', 'blitzCount', 'is_banned')