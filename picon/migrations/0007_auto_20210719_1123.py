# Generated by Django 3.2.2 on 2021-07-19 02:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picon', '0006_auto_20210718_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='index_name',
            field=models.CharField(max_length=50, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][a-z0-9]{6,19}$', '영어 소문자로 시작, 최소 7자 최대 20자까지 가능합니다.')]),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^(19|20)[0-9]{2}(1[0-2]|0[0-9])([0-2][0-9]|3[01])$', '생년월일을 바르게 입력해주세요.')]),
        ),
        migrations.AlterModelTable(
            name='feedback',
            table='feed_back',
        ),
    ]
