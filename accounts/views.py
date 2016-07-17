from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import BlitzUser
from .serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from django.core.files.images import ImageFile
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


from const import *
# Create your views here.

import json

class RegisterView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        json_data = json.loads(request.body)
        username    = json_data["username"]
        email       = json_data["email"]
        password    = json_data["password"]

        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "statusCode"    : HTTP_500_INTERNAL_SERVER_ERROR,
                    "details"       : "Username already exists."
                }
            )
        elif User.objects.filter(email=email).exists():
            return Response(
                {
                    "statusCode"    : HTTP_500_INTERNAL_SERVER_ERROR,
                    "details"       : "Email already exists."
                }
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        bUser= BlitzUser.objects.create(user=user)

        user.save()
        bUser.save()

        token = Token.objects.create(user=user)

        return Response(
            {
                "statusCode"    : HTTP_201_CREATED,
                "token"         : token.key,
            }
        )

class ProfileView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        serializedBlitzUser = ProfileBlitzUserSerializer(blitzUser)

        return Response(serializedBlitzUser.data)

class AvatarView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        file = request.FILES.get('filedata')
        image = ImageFile(file)

        #CHeck if file is an image

        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        blitzUser.avatar.save("amganagato.png", image)
        blitzUser.save()

        return Response(
            {
                "statusCode" : HTTP_200_OK
            }
        )

class ChangeUsernameView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user
        json_data = json.loads(request.body)
        newUsername = json_data["newUsername"]

        if User.objects.filter(username=newUsername).exists():
            return Response(
                {
                    "statusCode"    : HTTP_409_CONFLICT,
                    "details"       : "Username already exists."
                }
            )
        else:
            user.username = newUsername
            user.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response(
                {
                    "statusCode"    : HTTP_200_OK,
                    "token"         : token
                }
            )

class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        json_data = json.loads(request.body)
        oldPassword = json_data["oldPassword"]
        newPassword = json_data["newPassword"]

        username = request.user.username

        user = authenticate(username=username, password=oldPassword)

        if user is not None:
            user.set_password(newPassword)
            user.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response(
                {
                    "statusCode"    : HTTP_200_OK,
                    "token"         : token
                }
            )
        else:
            return Response(
                {
                    "statusCode"    : HTTP_400_BAD_REQUEST,
                    "details"       : "Wrong password."
                }
            )

class SearchUserView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        json_data   = json.loads(request.body)
        query       = json_data["query"]

        user = request.user
        userlist    = BlitzUser.objects.filter(user__username__icontains=query).exclude(user=user)

        serializedUserList = SearchBlitzUserSerializer(userlist, many=True, requestingUser=user.username)

        return Response(
            {
                "userList" : serializedUserList.data
            }
        )

class AddFollowView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        json_data       = json.loads(request.body)
        followedUser    = json_data["followedUser"]

        user            = request.user
        blitzUser       = BlitzUser.objects.get(user=user)

        try:
            blitzUser.follows.add(BlitzUser.objects.get(user__username=followedUser))
            blitzUser.save()
        except BlitzUser.DoesNotExist:
            return Response(
                {
                    "statusCode" : HTTP_404_NOT_FOUND
                }
            )

        return Response(
            {
                "statusCode" : HTTP_200_OK
            }
        )

class DelFollowView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        json_data = json.loads(request.body)
        followedUser = json_data["followedUser"]

        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        try:
            blitzUser.follows.remove(BlitzUser.objects.get(user__username=followedUser))
            blitzUser.save()
        except BlitzUser.DoesNotExist:
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

class GetFollowingView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        json_data = json.loads(request.body)
        client_pks = json_data["client_pks"] #From where to start counting users. Need to send 30 users at a time.
	
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        following = blitzUser.follows.all().exclude(pk__in=client_pks).order_by('-blitzCount')
        serializedFollowing = FollowingBlitzUserSerializer(following[0 : const.NUM_FOLLOWING_USERS], many=True, requestingUser=user.username)

        return Response(
            {
                "following" : serializedFollowing.data
            }
        )

class GetFollowersView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        json_data = json.loads(request.body)
        client_pks = json_data["client_pks"] # Get pk of users that are already in the client

        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        followers = BlitzUser.objects.filter(follows=blitzUser).exclude(pk__in=client_pks).order_by('blitzCount')
        serializedFollowers = BlitzUserSerializer(followers[0 : const.NUM_FOLLOWERS_USERS], many=True) #serialize only 30

        return Response(
            {
                "followers" : serializedFollowers.data
            }
        )

class VerifyTokenView(APIView):
	permission_classes = (permissions.IsAuthenticated, )
	
	def post(self, request, format=None):
		return Response(
			{
				"statusCode" : HTTP_200_OK
			}
		)
