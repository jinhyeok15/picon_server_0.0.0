from django.urls import path

from . import views


urlpatterns = [
    path('auth/success/', views.AuthSuccess.as_view()),
    path('register/', views.RegisterAccount.as_view()),
    path('register/info/', views.RegisterInfo.as_view()),
    path('quit/', views.QuitSession.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('savetok/', views.SaveToken.as_view()),
    path('<int:pk>/info/', views.ShowRegisterInfo.as_view()),
]
