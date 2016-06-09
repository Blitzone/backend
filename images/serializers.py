from rest_framework import serializers
from .models import Topic, Chapter, Blitz, UserTopic, UserChapter
from accounts.serializers import BlitzUserSerializer

class UserTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopic
        fields = ('id', 'user', 'topic', 'likes', 'dislikes')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'startDate', 'endDate')

class UserChapterSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('getUser')

    def getUser(self, userChapter):
<<<<<<< HEAD
        return serializers.serialize(userChapter.userTopic.user)
=======
        return BlitzUserSerializer(userChapter.userTopic.user).data
>>>>>>> 7ea2f4e3b826dccf0fb04aabc908b53e762c6fca

    class Meta:
        model = UserChapter
        fields = ('id', 'image', 'userTopic', 'chapter', 'user')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'topic')

class BlitzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blitz
        fields = ('id', 'user1', 'user2', 'winner', 'userTopic', 'startDate', 'endDate')
