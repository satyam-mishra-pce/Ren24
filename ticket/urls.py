from django.contrib import admin
from django.urls import path
from ticket import views

urlpatterns = [
    path('balance',views.balance,name='balance'),
    path('payment',views.payment,name='payment'),
    path('paymentpage',views.paymentpage,name='paymentpage'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('event', views.event, name='event'),
    path('qr/<uuid:ticketId>', views.qr, name='qr'),
    # path('success', views.purchase_ticket, name='success'),
    path('ticket/<uuid:event_id>', views.purchase_ticket, name='purchase_ticket'),
]
