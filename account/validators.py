# from django.contrib.auth.models import User
from picon.models import *
from picon.datasets import QuerySet, Element, Data
import re


def password_validation(pwd):
    if len(pwd) < 8:
        return '비밀번호는 최소 8자 이상이어야 합니다.'
    if re.search('[0-9]+', pwd) is None:
        return '비밀번호는 최소 1개 이상의 숫자가 포함되어야 합니다.'
    if re.search('[a-zA-Z]+', pwd) is None:
        return '비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 합니다.'
    if re.search('[`~!@#$%^&*]+', pwd) is None:
        return '비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.(`~!@#$%^&*).'
    return 'ok'


def index_name_validation(id_name):
    if re.search(r'^[a-z][a-z0-9]{6,19}$', id_name):
        return 'ok'
    return '영어 소문자로 시작, 최소 7자 최대 20자까지 가능합니다.'


def index_name_unique_validation(id_name):
    if User.objects.filter(username=id_name):
        return False
    return True


def nick_name_validation(nk):
    if re.search('[가-힣]+', nk):
        if len(nk) < 2:
            return '한글이 포함된 닉네임은 최소 2자 이상이어야 합니다.'
        if len(nk) > 8:
            return '한글이 포함된 닉네임은 최대 8자까지 가능합니다.'
        return 'ok'
    if len(nk) < 4:
        return '닉네임은 최소 4자 이상이어야 합니다.'
    if len(nk) > 12:
        return '닉네임은 최대 12자 까지 가능합니다.'
    return 'ok'
