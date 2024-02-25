from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'index.html')

def itinerary(request):
    return render(request,'itinerary.html')