import json
import time
from django.http import HttpResponseBadRequest,HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.models import User
from django.contrib.auth.decorators import login_required
# from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from ticket.functions import generate_ticket
from .models import *
# from config.settings import RAZORPAY_CLIENT,RAZOR_KEY_ID
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.


def qr(request,ticketId):
    ticket = generate_ticket(ticketId)
    response = HttpResponse(ticket, content_type='image/png')
    return response
    
def event(request):
    if request.method == 'GET':
        events = Events.objects.all()
        return render(request, 'events.html', {'events': events})

def getEvent(request):
    data = json.loads(request.body)
    event_id = data['event_id']
    event = Events.objects.get(id=event_id)
    context = {
        'id':event.id,
        'name':event.name,
        'desc':event.description,
        'amount':event.amount,
        'includedInPass':event.includedInPass,
    }
    return JsonResponse(context)

# def custom(request,ticketId):
#     ticket = CustomTicket.objects.filter(id=ticketId)
#     if ticket.exists():
#         ticket = ticket.first()
#         return
#     else:
#         return

