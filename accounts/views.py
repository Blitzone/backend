from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST

from .models import BlitzUser
from .serializers import BlitzUserSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from django.core.files.images import ImageFile
from django.contrib.auth import authenticate
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

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response(
            {
                "statusCode"    : HTTP_201_CREATED,
                "token"         : token,
            }
        )

class ProfileView(APIView):
    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        blitzUser = BlitzUser.objects.get(user=user)

        serializedBlitzUser = BlitzUserSerializer(blitzUser)

        return Response(serializedBlitzUser.data)

class AvatarView(APIView):
    parser_classes = (MultiPartParser, FormParser, )
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
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        json_data   = json.loads(request.body)
        query       = json_data["query"]

        userlist    = BlitzUser.objects.filter(user_username__icontains=query)

        serializedUserList = BlitzUserSerializer(userlist, many=True)

        return Response(
            {
                "userList" : serializedUserList.data
            }
        )