from django.urls import path
from cart import views

urlpatterns = [
    path('',views.cart,name='view_cart'),
    path('add',views.cart_add,name='cart_add'),
    path('delete',views.cart_delete,name='cart_delete'),
]
