from django.shortcuts import redirect, render

# Create your views here.

def home(request):
    return render(request,'index.html')

def itinerary(request):
    return render(request,'day1.html')

def itinerary_day(request,day):
    if day == 1:
        return render(request,'day1.html')
    elif day == 2:
        return render(request,'day2.html')
    elif day == 3:
        return render(request,'day3.html')
    else:
        return redirect('itinerary')