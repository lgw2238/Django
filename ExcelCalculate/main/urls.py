# main urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main_index'),
    path('signup', views.signup, name='main_signup'),
    path('signin', views.signin, name='main_signin'),
    path('verifyCode', views.verifyCode, name='main_verifyCode'),
    path('verify', views.verify, name='main_verify'),
    path('result', views.result, name='main_result'),
    path('signup/join', views.join, name='main_join'),
    path('signin/login', views.login, name='main_login'),
    path('logout', views.logout, name='main_logout'),
    path('loginFail', views.loginFail, name='main_loginFail'),




]

