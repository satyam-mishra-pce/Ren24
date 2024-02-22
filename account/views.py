# from email.message import EmailMessage
import base64
from django.shortcuts import get_object_or_404, render,redirect
# from account.forms import ProfileForm
from config import settings
from ticket.functions import generate_ticket
from ticket.models import Ticket
from .models import *
from django.contrib import messages
# from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
# from django.core.mail import EmailMessage, send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes,force_str
# from .tokens import generate_token
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# Create your views here.
import math, random
 
# function to generate OTP
def generateOTP() :
 
    # Declare a digits variable  
    # which stores all digits 
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def register(request):
    """Create a new user account and send a confirmation email."""
    # check if the request is a POST method
    if request.method == "POST":
        # get the input data from the request
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone Already Registered!!")
            return render(request, 'signup.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return render(request, 'register.html')
        
        myuser = User.objects.create(phone=phone, 
                                          first_name=fname,
                                          last_name=lname,
                                          password=pass1,
                                          is_active=False)
        myuser.save()
        
        # return a success message
        messages.success(request, "Your Account has been created succesfully!!")
        otp_obj,created = OTP.objects.get_or_create(user=myuser)
        otp_obj.otp = generateOTP()
        # TODO: Send OTP to phone number
        print("\n")
        print("\n")
        print(otp_obj.otp)
        print("\n")
        print("\n")
        otp_obj.save()
        return redirect('verify')
    
    # if the request is not a POST method, render a template with a form
    else:
        return render(request, 'signup.html')
    
def verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_obj = OTP.objects.filter(otp = otp)
        if otp_obj.exists():
            otp_obj =otp_obj.first()
            # TODO: Add expiration check on otp
            # print(datetime.now(),otp_obj.first().expiry)
            # if ((datetime.now())-otp_obj.first().expiry)>0:
            otp_obj.user.is_active = True
            otp_obj.user.save()
            login(request,otp_obj.user)
            return redirect('home')
            # else:
            #     messages.error(request,'OTP expired')
            #     return render(request, 'verify.html') 
        else:
            messages.error(request,'Wrong OTP')
            return render(request, 'verify.html') 
            
    else:
        return render(request, 'verify.html') 

def signin(request):
    if request.method=="POST":
        phone = request.POST.get('phone')
        password = request.POST.get('pass1')
        user=User.objects.filter(phone=phone)
        
        if user.exists():
            user = user.first()
            if (user.is_active==True):
                myuser=authenticate(request,phone=user.phone,password=password)
                print(myuser)
                if myuser is not None:
                    print('sahi baat hai')
                    login(request,myuser)
                    messages.success(request,"Logged IN Sucessfully")
                    print('done')
                    return redirect('home')
                else:   
                    messages.error(request, "Incorrect Password")
                    return render(request,"login.html")
            else:
                messages.error(request, "User not verified")
                return render(request,"login.html")
        else:
            messages.error(request, "User does not exist")
            return render(request,"login.html")
    else:
        return render(request,"login.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully")
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'GET':
        # get the current user's profile or create a new one
        profile, created = Profile.objects.get_or_create(user=request.user)
        # render the template with the profile data
        tickets = Ticket.objects.filter(user=request.user)
        ticket_img = []
        for ticket in tickets:
            ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
        context = {
            'profile':profile,
            'tickets':ticket_img
        }
        return render(request, 'profile.html',context)
    elif request.method == 'POST':
        return 
