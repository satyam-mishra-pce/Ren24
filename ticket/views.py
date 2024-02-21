import json
import time
from django.http import HttpResponseBadRequest,HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.models import User
from django.contrib.auth.decorators import login_required
# from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from .models import *
from config.settings import RAZORPAY_CLIENT,RAZOR_KEY_ID
from django.contrib import messages
from django.shortcuts import get_object_or_404
from PIL import Image
import qrcode
from io import  BytesIO
import base64
from PIL import ImageDraw, ImageFont
# Create your views here.


def home(request):
    return render(request,'index.html')

# @login_required
# def balance(request):
#     # load only the balance field and defer the rest
#     wallet = Wallet.objects.only('balance').get(user__id=request.user.id)
#     request.session['balance'] = wallet.balance
#     return render(request,'balance.html')


    
@login_required
def qr(request,ticketId):
        try:
            ticket = Ticket.objects.filter(user=request.user,id=ticketId)
            if(ticket.exists()):
                ticket = ticket.first()
                qr_image = qrcode.make(str(ticket.id))
                bg = Image.new("RGB", (300,400), "white")
                bg.paste(qr_image,(50,50))
                font = ImageFont.truetype(font='roboto',size=36)
                text =f"{request.user.first_name} {request.user.first_name}"
                # textwidth, textheight = draw.textsize(,font)
                draw = ImageDraw.Draw(bg)
                margin = 10
                x = 100
                y = 200

                # draw watermark in the bottom right corner
                draw.text((x,y),text,font=font)
                
                fp = BytesIO()
                draw.save(fp, "PNG")
                context = {'qr_code': base64.b64encode(fp.getvalue()).decode('utf-8')}
                return render(request, 'qr.html', context)
        except Ticket.DoesNotExist:
            ticket = None
            return HttpResponse("please purchase ticket")
        
# @login_required
# def purchase_ticket(request, event_id):
#     event_instance = get_object_or_404(Events, id=event_id)
#     # user_wallet = Wallet.objects.get(user=request.user)

#     if user_wallet.balance >= event_instance.cost:

#         user_wallet.balance -= event_instance.cost
#         user_wallet.save()
#         messages.success(request, f"payment have been successful collect ur qr from the below link")
#         Transaction.objects.create(user=request.user,
#                                    amount=event_instance.cost,
#                                    type="debit",
#                                    is_paid=True,)
#         Ticket.objects.create(user =request.user, event=event_instance)
#         return redirect('event')
#     else:
#         messages.error(request, "insufficient balance")
#         return render(request, 'events.html')

def event(request):
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

