import json
import time
from django.http import HttpResponseBadRequest,HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.decorators import profile_required
from account.functions import getPass
from account.models import Passes, User
from django.contrib.auth.decorators import login_required
# from django.db import transaction
from ticket.functions import generate_ticket,generate_master_ticket
from ticket.send_ticket import send_email_thread
from .models import *
# from config.settings import RAZORPAY_CLIENT,RAZOR_KEY_ID
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.


def qr(request,ticketId):
    if request.user.is_authenticated():
        ticket = generate_master_ticket(request.user)
    else:
        _pass = Passes.objects.get(psid=ticketId)
        ticket = generate_master_ticket(User.objects.get(email=_pass.email))
    response = HttpResponse(ticket, content_type='image/png')
    return response
    
def event(request):
    if request.method == 'GET':
        # events = Events.objects.all()
        # return render(request, 'events.html', {'events': events})
        events = Events.objects.filter(type='tech').only('id','poster')
        return render(request,'event.html',{'events':events})
    
def event_type(request,type):
    if request.method == 'GET':
        # events = Events.objects.all()
        # return render(request, 'events.html', {'events': events})
        events = Events.objects.filter(type=type).only('id','poster')
        return render(request,'event.html',{'events':events})

def getEvent(request):
    data = json.loads(request.body)
    event_id = data['event_id']
    event = Events.objects.get(id=event_id)
    if 'user_id' not in data:
        context = {
            'id':event.id,
            'name':event.name,
            'desc':event.description,
            'amount':event.amount,
            'includedInPass':event.includedInPass,
        }
        return JsonResponse(context)
    user_id = data['user_id']
    if event.includedInPass:
        user = User.objects.get(id=user_id)
        _pass = getPass(user)
        includedInPass = False
        if _pass is not None:
            if event.type == 'tech' and _pass.technical is None:
                includedInPass = True
            elif event.type == 'splash' and _pass.splash is None:
                includedInPass = True            
        context = {
            'id':event.id,
            'name':event.name,
            'desc':event.description,
            'amount':event.amount,
            'includedInPass':includedInPass,
        }
    else:
        context = {
            'id':event.id,
            'name':event.name,
            'desc':event.description,
            'amount':event.amount,
            'includedInPass':False,
        }
    return JsonResponse(context)

@login_required
@profile_required('/u/profile')
def buy(request,eventId):
    user = request.user
    _pass = getPass(user)
    if _pass == None:
        messages.error(request,'Ren Pass not activated')
        return redirect('events')
    event = Events.objects.filter(id=eventId)
    if event.exists():
        event = event.first()
        _type = event.type
        if _type == 'tech' and _pass.technical != None:
            messages.error(request,'Technical event already used')
            return redirect('events')
        if _type == 'splash' and _pass.splash != None:
            messages.error(request,'Technical event already used')
            return redirect('events')
        if _type == 'tech':
            _pass.technical = event
            _pass.save()
            Ticket.objects.create(user=user,event=event)
            messages.success(request,f'Ticket for {event.name} generated succesfully !')
            return redirect('profile')
        if _type == 'splash':
            _pass.splash = event
            _pass.save()
            Ticket.objects.create(user=user,event=event)
            messages.success(request,f'Ticket for {event.name} generated succesfully !')
            return redirect('profile')
        

def custom(request,ticketId):
    ticket = CustomTicket.objects.filter(id=ticketId)
    if ticket.exists():
        ticket = ticket.first()
        return HttpResponse(ticket.generate_customticket(), content_type='image/png')
    else:
        messages.error('Invalid ticket id')
        return redirect('home')


        
