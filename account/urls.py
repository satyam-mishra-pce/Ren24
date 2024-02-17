from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    # path('',home,name='home'),
    path('register',register,name='register'),
    path('verify',verify,name='verify'),
    path('login',signin,name='login'),
    path('logout',signout,name='logout'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('profile',profile_view,name='profile'),
]