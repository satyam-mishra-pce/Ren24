from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('balance',balance,name='balance'),
    path('payment',payment,name='payment'),
    path('paymentpage',paymentpage,name='paymentpage'),
    path('paymenthandler/',paymenthandler,name='paymenthandler')
]
