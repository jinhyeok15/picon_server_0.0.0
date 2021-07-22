from rest_framework.serializers import ModelSerializer
# from rest_framework import serializers
# from rest_framework.serializers import FileField

from picon.models import *
from django.contrib.auth.models import User


class AccountRegisterSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('nick_name', 'status')


class AccountAuthSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'phone_number')


class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
