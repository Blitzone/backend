from rest_framework.status import *

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from django.core.files.images import ImageFile
import json, datetime
from django.contrib.auth.models import User
from accounts.models import BlitzUser
from .models import Topic, UserTopic, Chapter,UserChapter
from .serializers import *
from django.utils import timezone
from const import *
from django.db.models import Q

class UploadUserChapterView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        #Get the user
        user        = request.user
        blitzUser   = BlitzUser.objects.get(user=user)

        #Get the chapter
        json_data  = json.loads(request.POST.get('params'))
        chapterId  = json_data["chapter"]

        #Get the file
        file = request.POST.get('filedata')
        image = ImageFile(file)


        #TODO CHeck if file is an image

        #Find topic and userTopic to add the new chapter to.

        topic = Topic.objects.get(endDate__gt=timezone.now(), startDate__lte=timezone.now())
        try:
            userTopic = UserTopic.objects.get(user=blitzUser, topic=topic)
        except UserTopic.DoesNotExist:
            userTopic = UserTopic(user=blitzUser, topic=topic)
            userTopic.save()

        chapter = Chapter.objects.get(pk=chapterId)

        try:
            userChapter = UserChapter.objects.get(userTopic=userTopic, chapter=chapter)
            userChapter.image = image
            userChapter.save()
	    userTopic.timestampUpdated = timezone.now()
	    userTopic.save()
        except UserChapter.DoesNotExist:
            userChapter = UserChapter(image=image, userTopic=userTopic, chapter=chapter)
            userChapter.save()

        return Response(
            {
                "statusCode" : HTTP_201_CREATED,
		        "imageUrl"   : userChapter.image.url
            }
        )

    # def get(self, request, format=None):
    #     user        = request.user
    #     blitzUser   = BlitzUser.objects.get(user=user)
    #
    #
    #     # Get the chapter
    #     json_data   = json.loads(request.body)
    #     chapterId   = json_data["chapter"]
    #     topicId     = json_data["topic"]
    #
    #     topic = Topic.objects.get(pk=topicId)
    #     userTopic = UserTopic.objects.get(user=blitzUser, topic=topic)
    #     chapter = Chapter.objects.get(pk=chapterId)
    #     try:
    #         userChapter = UserChapter.objects.get(userTopic=userTopic, chapter=chapter)
    #         serializedUserChapter = UserChapterSerializer(userChapter)
    #         return Response(serializedUserChapter.data)
    #     except UserChapter.DoesNotExist:
    #         return Response (
    #             {
    #                 "statusCode" : HTTP_404_NOT_FOUND
    #             }
    #         )
    #

class GetUserChaptersView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        topic = Topic.objects.get(endDate__gt=timezone.now(), startDate__lte=timezone.now())

        try:
            userTopic = UserTopic.objects.get(user=blitzUser, topic=topic)
            userChapters = UserChapter.objects.filter(userTopic=userTopic)
            serializedUserChapters = UserChapterSerializer(userChapters, many=True)
            return Response(
                {
                    "userChapters" : serializedUserChapters.data,
                }
            )
        except UserChapter.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )
        except UserTopic.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )


class TopicView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        topic = Topic.objects.get(endDate__gte=timezone.now(), startDate__lte=timezone.now())
        serializedTopic = TopicSerializer(topic)

        chapters = Chapter.objects.filter(topic=topic)
        serializedChapters = ChapterSerializer(chapters, many=True)

        return Response(
            {
                "topic"     : serializedTopic.data,
                "chapters"  : serializedChapters.data
            }
        )

class ChaptersView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        json_data   = json.loads(request.body)
        topicId  = json_data["topic"]
        topic = Topic.objects.get(pk=topicId)
        chapters = Chapter.objects.filter(topic=topic)

        serializedChapters = ChapterSerializer(chapters, many=True)

        return Response(
		{
			"chapters" : serializedChapters.data
		}
	)

class SearchPhotoChapterView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)
        json_data = json.loads(request.body)
        topicId = json_data["topic"]
        chapterId = json_data["chapter"]

        topic = Topic.objects.get(pk=topicId)
        chapter = Chapter.objects.get(pk=chapterId)
        userChapters = UserChapter.objects.filter(chapter=chapter, userTopic__topic=topic).exclude(userTopic__user=blitzUser)

        serializedUserChapters = SearchUserChapterSerializer(userChapters, many=True, requestingUser=user.username)

        return Response(
            {
                "searchPhotoChapters" : serializedUserChapters.data
            }
        )

class DailyPhotoChapterView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        json_data = json.loads(request.body)
        client_pks = json_data["client_pks"] #From where to start counting users. Need to send 30 users at a time.

        topic = Topic.objects.get(endDate__gte=timezone.now(), startDate__lte=timezone.now())
        userTopics = UserTopic.objects.filter(user__followed_by=blitzUser, topic=topic).exclude(user__pk__in=client_pks)

        serializedUserTopics = DailyUserTopicSerializer(userTopics[0 : const.NUM_DAILY_USER_TOPICS], many=True, requestingUser=blitzUser)
        return Response(
            {
                "userTopics" : serializedUserTopics.data
            }
        )

class LikeTopicView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        blitzUser = BlitzUser.objects.get(user=request.user)

        json_data = json.loads(request.body)
        userPk = json_data["user"]

        bUser = BlitzUser.objects.get(pk=userPk)
        userTopic = UserTopic.objects.get(user=bUser)

        try:
            userTopic.likedBy.add(blitzUser)
            userTopic.save()
        except UserTopic.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )
        #TODO check if user is disliked before liking, or if user doesn't exist etc.
        return Response(
            {
                "statusCode": HTTP_200_OK
            }
        )

class UnLikeTopicView(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        blitzUser = BlitzUser.objects.get(user=request.user)

        json_data = json.loads(request.body)
        userPk = json_data["user"]

        bUser = BlitzUser.objects.get(pk=userPk)
        userTopic = UserTopic.objects.get(user=bUser)

        try:
            userTopic.likedBy.remove(blitzUser)
            userTopic.save()
        except UserTopic.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )
        return Response(
            {
                "statusCode": HTTP_200_OK
            }
        )


class DisLikeTopicView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        blitzUser = BlitzUser.objects.get(user=request.user)

        json_data = json.loads(request.body)
        userPk = json_data["user"]

        bUser = BlitzUser.objects.get(pk=userPk)

        userTopic = UserTopic.objects.get(user=bUser)

        try:
            userTopic.dislikedBy.add(blitzUser)
            userTopic.save()
        except UserTopic.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )

        return Response(
            {
                "statusCode": HTTP_200_OK
            }
        )

class UnDisLikeTopicView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        blitzUser = BlitzUser.objects.get(user=request.user)

        json_data = json.loads(request.body)
        userPk = json_data["user"]

        bUser = BlitzUser.objects.get(pk=userPk)

        userTopic = UserTopic.objects.get(user=bUser)

        try:
            userTopic.dislikedBy.remove(blitzUser)
            userTopic.save()
        except UserTopic.DoesNotExist:
            return Response(
                {
                    "statusCode": HTTP_404_NOT_FOUND
                }
            )

        return Response(
            {
                "statusCode": HTTP_200_OK
            }
        )

class SendBlitzView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        requestingUser  = BlitzUser.objects.get(user=request.user)

        json_data       = json.loads(request.body)
        userPk          = json_data["user"]
        #challengeText   = json_data["text"]

        blitzedUser     = BlitzUser.objects.get(pk=userPk)


        topic = Topic.objects.get(endDate__gt=timezone.now(), startDate__lte=timezone.now())

        if not Blitz.objects.filter(Q(user1=requestingUser, user2=blitzedUser) | Q(user1=blitzedUser, user2=requestingUser)).count() > 0:
            #blitz = Blitz(user1=requestingUser, user2=blitzedUser, topic=topic, challengeText=challengeText)
            blitz = Blitz(user1=requestingUser, user2=blitzedUser, topic=topic)
	    blitz.save()
            return Response(
                {
                    "statusCode" : HTTP_200_OK
                }
            )
        else:
            return Response(
                {
                    "statusCode" : HTTP_409_CONFLICT
                }
            )
