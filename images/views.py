from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from django.core.files.images import ImageFile
import json, datetime
from accounts.models import BlitzUser
from .models import Topic, UserTopic, Chapter,UserChapter
from .serializers import TopicSerializer, ChapterSerializer, UserChapterSerializer
from django.utils import timezone

class UserChapterView(APIView):
    parser_classes = (MultiPartParser, FormParser, )
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

        topic = Topic.objects.get(endDate__gte=datetime.datetime.now(), startDate__lte=datetime.datetime.now())
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
        except UserChapter.DoesNotExist:
            userChapter = userChapter(image=image, userTopic=userTopic, chapter=chapter)
            userChapter.save()

        return Response(
            {
                "statusCode" : HTTP_201_CREATED
            }
        )

    def get(self, request, format=None):
        user        = request.user
        blitzUser   = BlitzUser.objects.get(user=user)


        # Get the chapter
        json_data   = json.loads(request.body)
        chapterId   = json_data["chapter"]
        topicId     = json_data["topic"]

        topic = Topic.objects.get(pk=topicId)
        userTopic = UserTopic.objects.get(user=blitzUser, topic=topic)
        chapter = Chapter.objects.get(pk=chapterId)
        try:
            userChapter = UserChapter.objects.get(userTopic=userTopic, chapter=chapter)
            serializedUserChapter = UserChapterSerializer(userChapter)
            return Response(serializedUserChapter.data)
        except UserChapter.DoesNotExist:
            return Response (
                {
                    "statusCode" : HTTP_404_NOT_FOUND
                }
            )



class TopicView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        topic = Topic.objects.get(endDate__gte=timezone.now(), startDate__lte=timezone.now())
        serializedTopic = TopicSerializer(topic)

        return Response(serializedTopic.data)

class ChaptersView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        json_data   = json.loads(request.body)
        topicId  = json_data["topic"]
        topic = Topic.objects.get(pk=topicId)
        chapters = Chapter.objects.filter(topic=topic)

        serializedChapters = ChapterSerializer(chapters, many=True)

        return Response(serializedChapters.data)
