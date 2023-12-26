import json
from django.shortcuts import redirect, render
from account.models import User,Wallet
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required
def balance(request):
    # load only the balance field and defer the rest
    wallet = Wallet.objects.only('balance').get(pk=request.user)
    request.session['balance'] = wallet.balance()
    print(request.session.get('balance'))
    return redirect('balance')

