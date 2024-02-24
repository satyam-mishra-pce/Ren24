from django.contrib import admin
from django.urls import path
from ticket import views

urlpatterns = [
    path('events', views.event, name='events'),
    path('getevent', views.getEvent, name='getevent'),
    path('qr/<uuid:ticketId>', views.qr, name='qr'),
    path('custom/<uuid:ticketId>', views.custom)
]
