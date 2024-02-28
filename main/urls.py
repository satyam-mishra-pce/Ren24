from django.urls import path
from main import views

urlpatterns = [
    path('',views.home,name='home'),
    path('itinerary',views.itinerary,name='itinerary'),
    path('itinerary/<int:day>',views.itinerary_day),
]
