# from email.message import EmailMessage
import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
import pytz
from account.forms import ProfileForm
# from account.forms import ProfileForm
from config import settings
from ticket.functions import generate_ticket
from ticket.models import Ticket
from .models import *
from django.contrib import messages
# from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
import pyotp
import datetime
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
    secret=pyotp.random_base32()
    otp = pyotp.TOTP(secret)
    return otp.now()


def register(request):
    """Create a new user account and send a confirmation email."""
    # check if the request is a POST method
    if request.method == "POST":
        # get the input data from the request
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        user_exist=User.objects.filter(email=email)
        if  (len(user_exist)>0):
            messages.error(request, "Email Already Registered!!")
            return render(request, 'login.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return render(request, 'signup.html')
        myuser = User.objects.create(email=email, 
                                          first_name=fname,
                                          last_name=lname,
                                          password=pass1,
                                          is_active=False)
        myuser.save()
        request.session['id'] = myuser.id
        
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
        otp_obj.created = datetime.datetime.now(pytz.UTC)
        otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(seconds=30)
        otp_obj.save()
        return redirect('verify')
    
    # if the request is not a POST method, render a template with a form
    else:
        return render(request, 'signup.html')




def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        user = User.objects.filter(email=email).first()  # Use .first() instead of .exists()

        if user:
            if user.is_active:
                myuser = authenticate(request, id=user.id, password=password)
                if myuser is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully")
                    request.session['id'] = user.pk
                    return redirect('home')
                else:   
                    messages.error(request, "Incorrect Password")
                    return render(request,"login.html")
            else:
                messages.error(request, "User not verified")
                request.session['id'] = user.pk
                otp_obj,created = OTP.objects.get_or_create(user=user.pk)
                otp_obj.otp = generateOTP()  # Implement your OTP generation logic
                # TODO: Send OTP to phone number
                print("\n")
                print("\n")
                print(otp_obj.otp)
                print("\n")
                print("\n")
                otp_obj.created = datetime.datetime.now(pytz.UTC)
                otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(seconds=30)
                otp_obj.save()
                return redirect("verify")
        else:
            messages.error(request, "User does not exist")
            return render(request, "signup.html")
    else:
        return render(request, "login.html")




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
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        phone=request.POST.get("phone")
        dob=request.POST.get("dob")
        sem=request.POST.get("sem")
        college=request.POST.get("college")
        address=request.POST.get("address")
        user_obj=User.objects.get(id=request.session.get("id"))
        profile_obj=Profile.objects.get(user=user_obj)
        user_obj.first_name=first_name
        user_obj.last_name=last_name
        profile_obj.phone=phone
        profile_obj.dob=dob
        profile_obj.sem=sem
        profile_obj.college=college
        profile_obj.address=address
        profile_obj.user
        profile_obj.save()
        user_obj.save()
        profile =request.user.profile
        # render the template with the profile data
        tickets = Ticket.objects.filter(user=request.user)
        ticket_img = []
        for ticket in tickets:
            ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
        context = {
            'profile':profile,
            'tickets':ticket_img
        }
        messages.success(request,"Profile updated Sucessfully")
        return render(request,"profile.html",context)
          


def resendOTP(request):
    myuser=User.objects.get(id=request.session.get("id"))
    otp_obj= OTP.objects.get(user=myuser)
    otp_obj.otp = generateOTP()
    otp_obj.created = datetime.datetime.now(pytz.UTC)
    otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(seconds=30)
    otp_obj.save()
    # TODO: Send OTP to phone number
    print("\n")
    print("\n")
    print(otp_obj.otp)
    print("\n")
    print("\n")
    otp_obj.save()
    return redirect('verify')

def verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.get(id=request.session.get("id"))  # Use get() to avoid KeyError
        otp_obj = OTP.objects.filter(user=user).first()  # Use filter() to handle None case
        check_otp=str(otp_obj.otp)
        if otp==check_otp:  
            if datetime.datetime.now(pytz.UTC) > otp_obj.expire:
                messages.warning(request, "OTP has expired")
                # return redirect('')
                return resendOTP(request)
            user.is_active=True
            user.save()
            login(request, user)
            return redirect('home')
            
        else:
            messages.error(request, 'Wrong OTP')
            return redirect('signup')
    else:
        return render(request, 'verify.html')
    
def image_upload(request):
    if request.method=='POST':
        profile= Profile.objects.get(user=request.user)
    # if the request method is POST, process the form data
        # create a form instance and populate it with data from the request
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # check whether the form is valid
        if form.is_valid():
            # save the form data to the database
            form.save()
            # redirect to the same page
            return redirect('profile')
        # render the template with the profile data
        tickets = Ticket.objects.filter(user=request.user)
        ticket_img = []
        for ticket in tickets:
            ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
        context = {
            'profile':profile,
            'tickets':ticket_img
        }
        messages.success(request,"Profile updated Sucessfully")
        return render(request,"profile.html",context)
    else:
        return render(request,"profile.html")