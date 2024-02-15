from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register',register,name='register'),
    path('signin',signin,name='signin'),
    path('signout',signout,name='signout'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('profile',profile_view,name='profile'),
    path('editprofile',editprofile,name='editprofile'),
]