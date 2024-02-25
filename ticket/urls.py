from django.contrib import admin
from django.urls import path
from ticket import views
from ticket import api

urlpatterns = [
    path('events', views.event, name='events'),
    path('getevent', views.getEvent, name='getevent'),
    path('qr/<uuid:ticketId>', views.qr, name='qr'),
    path('custom/<uuid:ticketId>', views.custom),
    path('api/verify',api.verify),
    path('api/permit',api.permit),
]
