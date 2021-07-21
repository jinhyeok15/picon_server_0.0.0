from django.contrib import admin
from. import models

# Register your models here.

admin.site.register(models.Follow)
admin.site.register(models.File)
admin.site.register(models.FeedBack)
admin.site.register(models.Pick)


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'user_pk', 'index_name', 'created'
    ]

    def short_content(self, post):
        return post.content[:10]


@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'birthday', 'sex', 'address'
    ]

    def short_content(self, post):
        return post.content[:10]
