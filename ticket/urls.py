from django.contrib import admin
from django.urls import path
from ticket import views

urlpatterns = [
    path('',views.home,name='home'),
    path('payment',views.payment,name='payment'),
    path('paymentpage',views.paymentpage,name='paymentpage'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('events', views.event, name='events'),
    path('getevent', views.getEvent, name='getevent'),
    path('qr/<uuid:ticketId>', views.qr, name='qr'),
    # path('success', views.purchase_ticket, name='success'),
    # path('ticket/<uuid:event_id>', views.purchase_ticket, name='purchase_ticket'),
]
