import json
from django.http import HttpResponse
from django.shortcuts import render
from cart.cart import Cart
from cart.functions import getPass

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
