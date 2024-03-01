from django.shortcuts import redirect, render

from ticket.models import Events

# Create your views here.

def home(request):
    return render(request,'index (1).html')

def itinerary(request):
    return render(request,'day1.html')

def celebrity(request):
    return render(request,'celebrities.html')

# def e(request):
#     events = Events.objects.all().only('id','poster')
#     return render(request,'event.html',{'events':events})

def itinerary_day(request,day):
    if day == 1:
        return render(request,'day1.html')
    elif day == 2:
        return render(request,'day2.html')
    elif day == 3:
        return render(request,'day3.html')
    else:
        return redirect('itinerary')