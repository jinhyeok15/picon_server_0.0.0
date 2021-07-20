from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
# Create your models here.


class User(models.Model):
    index_name = models.CharField(max_length=50, null=True, unique=True, validators=
                                  [RegexValidator(r'^[a-z][a-z0-9]{6,19}$',
                                                  '영어 소문자로 시작, 최소 7자 최대 20자까지 가능합니다.')])
    pw = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    nick_name = models.CharField(max_length=32, null=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    phone_number = models.CharField(max_length=50, null=True, unique=True,
                                    validators=[
                                        RegexValidator(
                                            r'^0[0-9]{2}-[0-9]{4}-[0-9]{4}$', '유효하지 않은 전화번호 형식입니다.'
                                        )])
    status = models.SmallIntegerField(default=0)  # 계정 미수락:0, 정상:1, 회원탈퇴:4

    class Meta:
        db_table = 'user'
        ordering = ['created']


class UserInfo(models.Model):
    user = models.OneToOneField('User', related_name="user_info", on_delete=models.CASCADE)
    birthday = models.CharField(max_length=16, validators=[
        RegexValidator(r'^(19|20)[0-9]{2}(1[0-2]|0[0-9])([0-2][0-9]|3[01])$', '생년월일을 바르게 입력해주세요.')
    ])
    sex = models.CharField(max_length=1)  # M/F
    address = models.CharField(max_length=200, null=True)


class Follow(models.Model):
    from_follow = models.ForeignKey('User', related_name='from_follow', on_delete=models.CASCADE)
    to_follow = models.ForeignKey('User', related_name='to_follow', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)  # 정상:1, 삭제:4
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'follow'
        constraints = [
            models.UniqueConstraint(fields=['from_follow', 'to_follow'], name='unique_relation')
        ]


class File(models.Model):
    user = models.ForeignKey('User', related_name='file', on_delete=models.CASCADE)
    file_url = models.CharField(max_length=512, unique=True)
    comment = models.CharField(max_length=200, null=True)
    status = models.SmallIntegerField(default=1)  # status = 0:삭제, 1:정상, 2:과거 프로필
    created = models.DateTimeField(auto_now_add=True)
    is_profile = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=10)  # 파일 업로드시 type. 'image', 'video'

    class Meta:
        db_table = 'file'


class FeedBack(models.Model):
    from_feed_back = models.ForeignKey('User', related_name='from_feed_back', on_delete=models.CASCADE)
    to_feed_back = models.ForeignKey('File', related_name='to_feed_back', on_delete=models.CASCADE)
    # 피드백 이모티콘 종류 (heart, like, bad, sad, happy)
    type = models.CharField(max_length=10, default='heart')
    status = models.SmallIntegerField(default=1)  # 1 정상, 4 삭제
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feed_back'


class Pick(models.Model):
    from_pick = models.ForeignKey('User', related_name='from_pick', on_delete=models.CASCADE)
    to_pick = models.ForeignKey('File', related_name='to_pick', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)  # 1 정상, 4 삭제
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pick'