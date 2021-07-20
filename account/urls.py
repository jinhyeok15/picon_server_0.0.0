from django.urls import path

from . import views


urlpatterns = [
    path('auth/success', views.AuthSuccess.as_view()),
    path('register', views.Register.as_view()),
    path('register/info', views.RegisterInfo.as_view()),
]
