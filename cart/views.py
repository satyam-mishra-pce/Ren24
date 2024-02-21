import json
from .models import *
from django.http import HttpResponse
from django.shortcuts import render
from cart.cart import Cart
from cart.functions import getPass
from django.contrib.auth.decorators import login_required
from config.settings import RAZORPAY_CLIENT,RAZOR_KEY_ID
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import time
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest,HttpResponse, JsonResponse
from ticket.views import qr

# Create your views here.
def cart(request):
    if request.method == 'GET':
        cart = Cart(request)
        added_events = list(cart.get())
        total = cart.cart_total()
        discount = 0
        _pass = getPass(request.user)
        if _pass != None:
            if _pass.technical1 == None:
                for event in added_events:
                    if event.type == 'tech' and event.includedInPass:
                        discount += event.amount
                        added_events.remove(event)
                        break;
            if _pass.technical2 == None:
                for event in added_events:
                    if event.type == 'tech' and event.includedInPass:
                        discount += event.amount
                        added_events.remove(event)
                        break;
            if _pass.splash == None:
                for event in added_events:
                    if event.type == 'splash' and event.includedInPass:
                        discount += event.amount
                        added_events.remove(event)
                        break;
        nett_amount = total - discount
        request.session['nett_amount'] = nett_amount
        context = {
            'events':cart.get(),
            'nett':nett_amount,
            'total':total,
            'discount':discount,
            'payment_required': True if discount !=0 else False
        }
        return render(request,'cart.html',context)
    
    
def cart_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            event_id = data['event_id']
            print(event_id)
            Cart(request).add(int(event_id))
            return HttpResponse("Item added to cart successfully !",status=200)
        except Exception as e:
            print(e)
            return HttpResponse("Unexpected error occured !",status=500)
    
    
def cart_delete(request):
    if request.method == 'POST':
        try :
            data = json.loads(request.body)
            # event_id = request.POST.get('event_id')
            event_id = data['event_id']
            Cart(request).delete(int(event_id))
            return HttpResponse("Item deleted from cart successfully !",status=200)
        except Exception as e:
            print(e)
            return HttpResponse("Unexpected error occured !",status=500)


def checkout(request):
    events = Cart(request).get()
    nett_amount = request.session.get('nett_amount')
    if nett_amount==0:
        context = {
        "events":events,
        "netTotal":nett_amount,
        }
        Cart(request).generate_ticket()
        return 
    return redirect(paymentpage)



@login_required
def paymentpage(request):
    currency = 'INR'
    amount =  request.session.get('nett_amount') # Rs. 200
    amount=int(float(amount)*100)

    # Create a Razorpay Order
    razorpay_order = RAZORPAY_CLIENT.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    Transaction.objects.create(order_id=razorpay_order['id'],
                                    amount=amount//100,
                                    user=request.user,
                                    )
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
                    paymentobj.save()
                    messages.success(request,"Payment Sucessful!!")
                    Cart(request).generate_ticket()
                    return redirect('home')
            
                except Exception as e:

                    # if there is an error while capturing payment.
                    print(e)
                    messages.success(request,"Payment Fail!!")
                    return redirect('home')
            else:

                # if signature verification fails.
                messages.success(request,"Payment Fail!!")
                return redirect('home')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
            