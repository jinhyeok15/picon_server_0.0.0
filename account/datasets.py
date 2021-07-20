from picon.models import *
from config.res import *
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class QuerySet:
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
    def _get_obj(obj, pk, key):
        try:
            if type(pk) == list:
                element = list(map(lambda x: obj.objects.filter(pk=x).values(key), pk))
            else:
                element = obj.objects.filter(pk=pk).values(key)
            return element
        except ObjectDoesNotExist:
            raise Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_element_from_obj(obj, key):
        if type(obj) == list:
            field = []
            for i in obj:
                try:
                    element = i[0][key]
                except IndexError:
                    element = None
                field.append(element)
            return field
        return obj[0][key]


class Data(Element):
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
