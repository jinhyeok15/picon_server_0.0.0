from django.shortcuts import render
from .validators import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config import res
from . import serializers
from picon.models import *
import uuid
# Create your views here.


# class Auth(APIView):


class AuthSuccess(APIView):
    user_serializer = serializers.UserSerializer

    def post(self, request):
        code = str(uuid.uuid4())
        if request.data['auth_type'] == 'email':
            serializer = self.user_serializer(
                data={'email': request.data['input'],
                      'code': code}
            )
            if serializer.is_valid():
                serializer.save()
                user_id = User.objects.filter(code=code).values('id')[0]['id']
                return Response(response_data(201, res.AUTH_SUCCESS, id=user_id), status.HTTP_201_CREATED)
            return Response(response_data(400, res.NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)
        if request.data['auth_type'] == 'phone':
            serializer = self.user_serializer(
                data={'phone_number': request.data['input'],
                      'code': code}
            )
            if serializer.is_valid():
                serializer.save()
                user_id = User.objects.filter(code=code).values('id')[0]['id']
                return Response(response_data(201, res.AUTH_SUCCESS, id=user_id), status.HTTP_201_CREATED)
            return Response(response_data(400, res.NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)
        return Response(response_data(400, res.AUTH_FAIL), status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    user_serializer = serializers.UserSerializer

    def post(self, request):
        try:
            queryset = User.objects.get(pk=request.data['id'])
        except User.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        request.data['status'] = 1
        serializer = self.user_serializer(queryset, data=request.data)
        if serializer.is_valid():
            if password_validation(request.data['pw']) != 'ok':
                return Response(response_data(200, password_validation(request.data['pw'])),
                                status.HTTP_200_OK)
            if request.data['pw'] != request.data['valid_pw']:
                return Response(response_data(200,
                                              '비밀번호가 일치하지 않습니다.'), status.HTTP_200_OK)
            if nick_name_validation(request.data['nick_name']) != 'ok':
                return Response(response_data(200, nick_name_validation(request.data['nick_name'])),
                                status.HTTP_200_OK)
            serializer.save()
            return Response(response_data(201, res.CREATED, id=request.data['id']), status.HTTP_201_CREATED)
        return Response(response_data(400, res.NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)


class RegisterInfo(APIView):
    user_info_serializer = serializers.UserInfoSerializer

    def post(self, request):
        serializer = self.user_info_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(201, res.REGISTERED, id=int(request.data['user'])), status.HTTP_201_CREATED)
        return Response(response_data(400, res.NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)
