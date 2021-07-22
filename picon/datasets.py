from .models import *
from config.res import *
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class QuerySet:
    @staticmethod
    def get_obj(obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_account(pk):
        try:
            return Account.objects.get(user=pk)
        except Account.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_user_info(pk):
        try:
            return UserInfo.objects.get(user=pk)
        except UserInfo.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @classmethod
    def user_follow(cls, user_id):
        obj = Follow.objects.filter(from_follow=user_id).values('to_follow')
        try:
            user_follow_list = []
            for i in obj:
                user_follow_list.append(i['to_follow'])
            return user_follow_list
        except IndexError:
            return []

    @classmethod
    def user_file(cls, user_id):
        obj = File.objects.filter(user=user_id).values('id')
        try:
            user_file_list = []
            for i in obj:
                user_file_list.append(i['id'])
            return user_file_list
        except IndexError:
            return []


class Element:

    @staticmethod
    def _get_obj_by_key(obj, pk, key):  # pk와 오브젝트가 주어지면 key 이름에 해당하는 필드 obj return
        try:
            if type(pk) == list:
                return list(map(lambda x: obj.objects.filter(pk=x).values(key), pk))
            return obj.objects.filter(pk=pk).values(key)
        except ObjectDoesNotExist:
            raise Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_element_from_obj(obj, key):  # 요소 obj가 주어지면 obj 값 return
        if type(obj) == list:
            field = []
            for i in obj:
                if i:
                    field.append(i[0][key])
                else:
                    field.append(None)
            return field
        return obj[0][key]


class Data(Element):  # 필드 리스트와 element 값 리스트가 주어지면 dataset 리턴
    @staticmethod
    def _set_data(fields, elements):
        cnt = 0
        try:
            data_list = []
            while cnt < len(elements[0]):
                record = [i[cnt] for i in elements]
                data = dict(zip(fields, record))
                data_list.append(data)
                cnt += 1
            return data_list
        except IndexError:
            data = dict(zip(fields, elements))
            return data
