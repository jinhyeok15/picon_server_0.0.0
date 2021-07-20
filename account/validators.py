from picon.models import *
from .datasets import *
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
