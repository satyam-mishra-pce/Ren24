import json
import time
from django.http import HttpResponseBadRequest,HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.models import User
from django.contrib.auth.decorators import login_required
# from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
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
def payment(request):
    return render(request,'payment.html')

@login_required
def paymentpage(request):
    currency = 'INR'
    amount = request.POST.get('amount') # Rs. 200
    if amount is None:
        amount=100
    else:
        amount=int(float(amount)*100)

    # Create a Razorpay Order
    razorpay_order = RAZORPAY_CLIENT.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    Transaction.objects.create(order_id=razorpay_order['id'],
                                    amount=amount//100,
                                    user=request.user,
                                    type="credit")
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    # render the payment.html template with the context
    return render(request, 'razorpay.html', context=context)





# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@login_required
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:
        
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = RAZORPAY_CLIENT.utility.verify_payment_signature(params_dict)
            if result is True:
                paymentobj = Transaction.objects.get(order_id=razorpay_order_id)
                amount=paymentobj.amount*100
                try:
                    # # get the user's wallet
                    # user_wallet = Wallet.objects.get(user=request.user)
                    # # update the wallet balance
                    # user_wallet.balance += amount//100
                    # user_wallet.save()
                    
                    # capture the payment
                    RAZORPAY_CLIENT.payment.capture(payment_id, amount)
                    
                    # render success page on successful capture of payment
                    paymentobj.is_paid=True
                    messages.success(request,"Payment Sucessful!!")
                    time.sleep(5)
                    return redirect('home')
            
                except Exception as e:

                    # if there is an error while capturing payment.
                    messages.success(request,"Payment Fail!!")
                    time.sleep(5)
                    return redirect('home')
            else:

                # if signature verification fails.
                messages.success(request,"Payment Fail!!")
                time.sleep(5)
                return redirect('home')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
    
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