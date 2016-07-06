from rest_framework import serializers
from .models import Topic, Chapter, Blitz, UserTopic, UserChapter
from accounts.serializers import BlitzUserSerializer
from accounts.models import BlitzUser

class UserTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopic
        fields = ('id', 'user', 'topic', 'likes', 'dislikes')

class DailyUserTopicSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('getUsername')
    photoChapters = serializers.SerializerMethodField('getPhotoChapters')
    is_liked = serializers.SerializerMethodField('isLiked')
    is_disliked = serializers.SerializerMethodField('isDisliked')

    def __init__(self, *args, **kwargs):
        self.requestingUser = kwargs.pop('requestingUser', None)
        super(DailyUserTopicSerializer, self).__init__(*args, **kwargs)

    def getUsername(self, userTopic):
        return BlitzUserSerializer(userTopic.user).data

    def getPhotoChapters(self, userTopic):
        photoChapters = UserChapter.objects.filter(userTopic=userTopic)
        return DailyUserChapterSerializer(photoChapters, many=True).data

    def isLiked(self, userTopic):
        blitzUser = BlitzUser.objects.get(user__username=self.requestingUser)
	t = UserTopic.objects.get(pk=userTopic.pk)
        return t in blitzUser.likes.all()

    def isDisliked(self, userTopic):
        blitzUser = BlitzUser.objects.get(user__username=self.requestingUser)
	t = UserTopic.objects.get(pk=userTopic.pk)
        return t in blitzUser.dislikes.all()

    class Meta:
        model = UserTopic
        fields = (
		'user', 
		'likes', 
		'dislikes', 
		'is_liked', 
		'is_disliked', 
		'photoChapters', 
		'timestampUpdated')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'startDate', 'endDate')

class UserChapterSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('getUser')

    def getUser(self, userChapter):
        return BlitzUserSerializer(userChapter.userTopic.user).data

    class Meta:
        model = UserChapter
        fields = ('id', 'image', 'userTopic', 'chapter', 'user')

class DailyUserChapterSerializer(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField('getChapter')

    def getChapter(self, userChapter):
        return userChapter.chapter.name
    class Meta:
        model = UserChapter
        fields = ('image', 'chapter')


class SearchUserChapterSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('getUser')
    is_followed = serializers.SerializerMethodField('isFollowed')

    def __init__(self, *args, **kwargs):
        self.requestingUser = kwargs.pop('requestingUser', None)
        super(SearchUserChapterSerializer, self).__init__(*args, **kwargs)

    def getUser(self, userChapter):
        return BlitzUserSerializer(userChapter.userTopic.user).data

    def isFollowed(self, userChapter):
        requestingBlitzUser = BlitzUser.objects.get(user__username=self.requestingUser)
        return userChapter.userTopic.user in requestingBlitzUser.follows.all()

    class Meta:
        model = UserChapter
        fields = ('id', 'image', 'userTopic', 'chapter', 'user', 'is_followed')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'name', 'topic')

class BlitzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blitz
        fields = ('id', 'user1', 'user2', 'winner', 'userTopic', 'startDate', 'endDate')
