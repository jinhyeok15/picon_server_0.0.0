from django.shortcuts import render
from .validators import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from config import res
from config.res import response_data, error_data
from .serializers import *
from picon.datasets import QuerySet
from picon.models import *
# from django.contrib.auth.models import User
import uuid
# Create your views here.
# jwt 데코레이터:
# from rest_framework.decorators import permission_classes, authentication_classes
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))

# class Auth(APIView):


class AuthSuccess(APIView):
    permission_classes = [AllowAny]  # 아직 토큰 발급받지 않은 API

    def post(self, request):
        name_uuid = str(uuid.uuid4())
        data = {  # 임시 계정 데이터 생성
            "username": f'{name_uuid}',
            "password": f'{name_uuid}'
        }
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():  # 임시 계정 데이터 User테이블에 저장
            serializer.save()
        try:
            user = User.objects.get(username=f'{name_uuid}')
        except User.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        try:
            queryset = Account.objects.get(user_pk=user.id)
        except Account.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        if request.data['auth_type'] == 'email':
            email_data = {'email': request.data['input']}
            serializer = AccountAuthSerializer(queryset, data=email_data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(201, res.AUTH_SUCCESS, id=user.id), status.HTTP_201_CREATED)
            user.delete()  # 데이터가 유효하지 않으면 유저 인스턴스 삭제
            return Response(error_data(400, res.NOT_VALID, serializer.errors), status.HTTP_400_BAD_REQUEST)
        if request.data['auth_type'] == 'phone':
            phone_data = {'phone_number': request.data['input']}
            serializer = AccountAuthSerializer(queryset, data=phone_data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(201, res.AUTH_SUCCESS, id=user.id), status.HTTP_201_CREATED)
            user.delete()
            return Response(error_data(400, res.NOT_VALID, serializer.errors), status.HTTP_400_BAD_REQUEST)
        return Response(response_data(400, res.NOT_VALID), status.HTTP_400_BAD_REQUEST)


class RegisterAccount(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_name = request.data['index_name']
        if index_name_validation(id_name) != 'ok':
            return Response(
                response_data(400, index_name_validation(id_name)),
                status.HTTP_400_BAD_REQUEST
            )
        if not index_name_unique_validation(id_name):
            return Response(
                response_data(400, '해당 유저가 이미 존재합니다.'),
                status.HTTP_400_BAD_REQUEST
            )
        password = request.data['pw']
        if password_validation(password) != 'ok':
            return Response(
                response_data(400, password_validation(password)),
                status.HTTP_400_BAD_REQUEST
            )
        if password != request.data['valid_pw']:
            return Response(
                response_data(400, '비밀번호가 일치하지 않습니다.'),
                status.HTTP_400_BAD_REQUEST
            )
        nick_name = request.data['nick_name']
        if nick_name_validation(nick_name) != 'ok':
            return Response(
                response_data(400, nick_name_validation(nick_name)),
                status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=request.data['id'])
            user.username = id_name
            if user.password != password:
                user.set_password(password)
            user.save()
        except User.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)
        try:
            queryset = Account.objects.get(user_pk=request.data['id'])
        except Account.DoesNotExist:
            return Response(
                response_data(404, res.NOT_EXIST_USER),
                status.HTTP_404_NOT_FOUND
            )
        account_data = {
            'nick_name': nick_name,
            'status': 1
        }
        serializer = AccountRegisterSerializer(queryset, data=account_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_data(201, res.REGISTERED, id=request.data['id']),
                status.HTTP_201_CREATED
            )
        return Response(
            error_data(400, res.NOT_VALID, serializer.errors),
            status.HTTP_400_BAD_REQUEST
        )


class RegisterInfo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(201, res.REGISTERED, id=request.data['user']), status.HTTP_201_CREATED)
        return Response(response_data(400, res.NOT_VALID), status.HTTP_400_BAD_REQUEST)


class QuitSession(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            queryset = User.objects.get(pk=request.data['id'])
            queryset.delete()
            return Response(response_data(204, res.DELETED), status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            queryset = User.objects.get(username=username)
            if queryset.check_password(password):
                return Response(
                    response_data(200, res.LOGIN_SUCCESS,
                                  username=username, password=password, id=queryset.id),
                    status.HTTP_200_OK
                )
            return Response(response_data(400, res.LOGIN_FAIL), status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(response_data(400, res.LOGIN_FAIL), status.HTTP_400_BAD_REQUEST)


class SaveToken(APIView):

    def post(self, request):
        try:
            queryset = Account.objects.get(user_pk=request.data['id'])
            queryset.code = request.data['code']
            queryset.save()
            return Response({}, status.HTTP_204_NO_CONTENT)
        except Account.DoesNotExist:
            return Response(response_data(404, res.NOT_EXIST_USER), status.HTTP_404_NOT_FOUND)


class ShowRegisterInfo(APIView):

    def get(self, request, pk):
        user = QuerySet.get_obj(User, pk)
        account = QuerySet.get_account(pk)
        user_info = QuerySet.get_user_info(pk)
        dataset = {
            'id': user.id,
            'index_name': user.username,
            'nick_name': account.nick_name,
            'email': account.email,
            'phone_number': account.phone_number,
            'name': user_info.name,
            'birthday': user_info.birthday,
            'sex': user_info.sex,
            'address': user_info.address
        }
        return Response(response_data(200, res.OK, data=dataset), status.HTTP_200_OK)
