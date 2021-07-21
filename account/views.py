from django.shortcuts import render
from .validators import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from config import res
from . import serializers
from picon.models import *
import uuid
# Create your views here.
# jwt 데코레이터:
# @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))

# class Auth(APIView):


class AuthSuccess(APIView):
    permission_classes = [AllowAny]  # 아직 토큰 발급받지 않은 API

    def post(self, request):
        try:
            account_id = max(list(map(lambda x: x['user_pk'], Account.objects.all().values('user_pk'))))+1
        except ValueError:
            account_id = 1
        data = {
            "username": f'username{account_id}',
            "password": f'password{account_id}'
        }
        serializer = serializers.CreateUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        try:
            user = User.objects.get(username=f'username{account_id}')
            user.username = f'username{user.id}'  # account_id가 pk와 같지 않을 경우 조정
            user.password = f'password{user.id}'
            user.save()
        except User.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        try:
            queryset = Account.objects.get(user_pk=user.id)
        except Account.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        if request.data['auth_type'] == 'email':
            email_data = {'email': request.data['input']}
            serializer = serializers.AccountInputSerializer(queryset, data=email_data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(201, res.AUTH_SUCCESS, id=user.id), status.HTTP_201_CREATED)
            user.delete()  # 데이터가 유효하지 않으면 유저 인스턴스 삭제
            return Response(error_data(400, res.NOT_VALID, serializer.errors), status.HTTP_400_BAD_REQUEST)
        if request.data['auth_type'] == 'phone':
            phone_data = {'phone_number': request.data['input']}
            serializer = serializers.AccountInputSerializer(queryset, data=phone_data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(201, res.AUTH_SUCCESS, id=user.id), status.HTTP_201_CREATED)
            user.delete()
            return Response(error_data(400, res.NOT_VALID, serializer.errors), status.HTTP_400_BAD_REQUEST)
        return Response(response_data(400, res.NOT_VALID), status.HTTP_400_BAD_REQUEST)


# class Login(APIView):
#     def post(self, request):

