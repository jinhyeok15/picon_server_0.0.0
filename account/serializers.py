from rest_framework.serializers import ModelSerializer
# from rest_framework.serializers import FileField

from picon.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
