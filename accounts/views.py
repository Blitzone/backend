from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_201_CREATED

from .models import BlitzUser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
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
                "details"       : "ok"
            }
        )
