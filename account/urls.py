from django.contrib import admin
from django.urls import path,include
from .views import *
import account.resetpass as reset

urlpatterns = [
    # path('',home,name='home'),
    path('register',register,name='register'),
    path('verify',verify,name='verify'),
    path('login',signin,name='login'),
    path('logout',signout,name='logout'),
    # path('activate/<uidb64>/<token>',activate,name='activate'),
    path('profile',profile_view,name='profile'),
    path('resendotp',reset.resendOTP,name='resendotp'),
    path('forgot',reset.forgotpassword,name='forgotpassword'),
    path('forgot/verify',reset.verify,name='resetpass_verify'),
    path('forgot/resendotp',reset.resendOTP,name= 'resetpass_resendotp'),
]