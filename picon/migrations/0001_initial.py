# Generated by Django 3.2.5 on 2021-07-21 06:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_pk', models.IntegerField(blank=True, null=True)),
                ('index_name', models.CharField(max_length=50, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][a-z0-9]{6,19}$', '영어 소문자로 시작, 최소 7자 최대 20자까지 가능합니다.')])),
                ('pw', models.CharField(max_length=50, null=True)),
                ('code', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nick_name', models.CharField(max_length=32, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=50, null=True, unique=True, validators=[django.core.validators.RegexValidator('^0[0-9]{2}-[0-9]{4}-[0-9]{4}$', '유효하지 않은 전화번호 형식입니다.')])),
                ('status', models.SmallIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.CharField(max_length=512, unique=True)),
                ('comment', models.CharField(max_length=200, null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_profile', models.SmallIntegerField(default=0)),
                ('type', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='picon.account')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^(19|20)[0-9]{2}(1[0-2]|0[0-9])([0-2][0-9]|3[01])$', '생년월일을 바르게 입력해주세요.')])),
                ('sex', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to='picon.account')),
            ],
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_pick', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_pick', to='picon.account')),
                ('to_pick', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_pick', to='picon.file')),
            ],
            options={
                'db_table': 'pick',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_follow', to='picon.account')),
                ('to_follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_follow', to='picon.account')),
            ],
            options={
                'db_table': 'follow',
            },
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='heart', max_length=10)),
                ('status', models.SmallIntegerField(default=1)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_feed_back', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_feed_back', to='picon.account')),
                ('to_feed_back', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_feed_back', to='picon.file')),
            ],
            options={
                'db_table': 'feed_back',
            },
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('from_follow', 'to_follow'), name='unique_relation'),
        ),
    ]
