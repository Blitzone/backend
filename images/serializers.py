from rest_framework import serializers
from .models import Topic, Chapter, Blitz, UserTopic, UserChapter

class UserTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopic
        fields = ('id', 'user', 'topic', 'likes', 'dislikes')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'startDate', 'endDate')

class UserChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChapter
        fields = ('id', 'image', 'userTopic', 'chapter')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'topic')

class BlitzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blitz
        fields = ('id', 'user1', 'user2', 'winner', 'userTopic', 'startDate', 'endDate')