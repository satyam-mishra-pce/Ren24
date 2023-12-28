import json
import time
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from account.models import User,Wallet
from django.contrib.auth.decorators import login_required
import razorpay
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import *
from config import settings
from django.contrib import messages
# Create your views here.

@login_required(login_url='signin')
def balance(request):
    # load only the balance field and defer the rest
    wallet = Wallet.objects.only('balance').get(user__id=request.user.id)
    request.session['balance'] = wallet.balance
    return render(request,'balance.html')

@login_required(login_url='signin')
def payment(request):
    return render(request,'payment.html')


razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url='signin')
def paymentpage(request):
    currency = 'INR'
    amount = request.POST.get('amount') # Rs. 200
    if amount is None:
        amount=100
    else:
        amount=int(float(amount)*100)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    RazorpayPayments.objects.create(order_id=razorpay_order['id'],
                                    amount=amount//100,
                                    user=request.user,
                                    type="credit")
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    # render the payment.html template with the context
    return render(request, 'razorpay.html', context=context)





# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@login_required(login_url='signin')
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
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is True:
                paymentobj = RazorpayPayments.objects.get(order_id=razorpay_order_id)
                amount=paymentobj.amount*100
                try:
                    # # get the user's wallet
                    user_wallet = Wallet.objects.get(userid=request.user)
                    # update the wallet balance
                    user_wallet.balance += amount//100
                    user_wallet.save()
                    
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)
                    
                    # render success page on successful capture of payment
                    paymentobj.is_paid=True
                    messages.success(request,"Payment Sucessful!!")
                    time.sleep(5)
                    return redirect('home')
                except:

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
    
