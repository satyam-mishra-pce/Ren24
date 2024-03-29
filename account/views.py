# from email.message import EmailMessage
import base64
import io
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
import pytz
from account.decorators import profile_required
from account.forms import ProfileForm
from account.functions import getPass
# from account.forms import ProfileForm
from config import settings
from ticket.functions import generate_master_ticket, generate_ticket
from ticket.models import Ticket
from ticket.send_ticket import send_email_thread
from .models import *
from django.contrib import messages
# from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
import pyotp
import datetime
from .email_otp import send_otp_thread
from PIL import Image
# from django.core.mail import EmailMessage, send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes,force_str
# from .tokens import generate_token
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# Create your views here.
# import math, random
 
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
        myuser = User.objects.create_user(email=email, 
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
        otp=otp_obj.otp
        print("\n")
        print("\n")
        otp_obj.created = datetime.datetime.now(pytz.UTC)
        otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
        otp_obj.save()
        send_otp_thread(email,otp)
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
                myuser = authenticate(request, id=user.id, password=password,)
                if myuser is not None:
                    login(request, user,backend="django.contrib.auth.backends.ModelBackend")
                    messages.success(request, "Logged in successfully")
                    request.session['id'] = user.pk
                    return redirect('home')
                else:   
                    messages.error(request, "Incorrect Password")
                    return render(request,"login.html")
            else:
                messages.error(request, "User not verified")
                request.session['id'] = user.pk
                otp_obj,created = OTP.objects.get_or_create(user=User.objects.get(email=email))
                otp_obj.otp = generateOTP()  # Implement your OTP generation logic
                # TODO: Send OTP to phone number
                print("\n")
                print("\n")
                otp=otp_obj.otp
                print(otp_obj.otp)
                print("\n")
                print("\n")
                otp_obj.created = datetime.datetime.now(pytz.UTC)
                otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
                otp_obj.save()
                send_otp_thread(email,otp)   
                return redirect("verify")
        else:
            messages.error(request, "User does not exist")
            return redirect('register')
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
        profile= Profile.objects.filter(user=request.user)
        if profile.exists():
            profile = profile.first()
        # render the template with the profile data
            tickets = Ticket.objects.filter(user=request.user)
            ticket_img = []
            for ticket in tickets:
                ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
            if profile.dob is not None:
                dob = profile.dob.strftime("%Y-%m-%d")
            else:
                dob = ''
            context = {
                'profile':profile,
                'dob':dob,
                'tickets':ticket_img
            }
            return render(request, 'profile.html',context)
        else:
            return render(request, 'profile.html')
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        phone=request.POST.get("phone")
        dob=request.POST.get("dob")
        rollno=request.POST.get("rollno")
        gender=request.POST.get("gender")
        college=request.POST.get("college")
        address=request.POST.get("address")
        image = request.FILES.get("image")
        user_obj=request.user
        profile_obj,created=Profile.objects.get_or_create(user=user_obj)
        user_obj.first_name=first_name
        user_obj.last_name=last_name
        profile_obj.phone=phone
        profile_obj.dob=dob
        profile_obj.rollno=rollno
        profile_obj.gender= genders.get(gender)
        profile_obj.college=college
        profile_obj.address=address
        # profile_obj.user
        print(image)
        if image is not None and image != "":
            profile_obj.image = image
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
            'dob':dob,
            'tickets':ticket_img
        }
        messages.success(request,"Profile updated Sucessfully")
        next = request.GET.get("next")
        if next:
            return redirect(next)
        return render(request,"profile.html",context)
          


def resendOTP(request):
    myuser=User.objects.get(id=request.session.get("id"))
    email=myuser.email
    otp_obj= OTP.objects.get(user=myuser)
    otp_obj.otp = generateOTP()
    otp_obj.created = datetime.datetime.now(pytz.UTC)
    otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
    otp=otp_obj.otp
    otp_obj.save()
    send_otp_thread(email,otp)
    # TODO: Send OTP to phone number
    print("\n")
    print("\n")
    print(otp_obj.otp)
    print("\n")
    print("\n")
    otp_obj.save()
    send_otp_thread(email,otp)   
    messages.sucess(request,"OTP sent sucessfully")
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
            login(request, user,backend="django.contrib.auth.backends.ModelBackend")
            return redirect('home')
            
        else:
            messages.error(request, 'Wrong OTP')
            return redirect('verify')
    else:
        return render(request, 'verify.html')

@login_required
@profile_required('/u/profile')
def send_ticket(request):
    if request.method=='POST':
        user=request.user
        _pass = getPass(user)
        if not _pass:
            messages.error(request,"You have not purchased any pass yet! Please register into event and try again later")
            return redirect('profile')
        email=user.email
        img=generate_master_ticket(user)
        image_buffer = io.BytesIO(img)
        image=Image.open(image_buffer)
        img_rgb=image.convert('RGB')
        pdf_buffer = io.BytesIO()
        img_rgb.save(pdf_buffer, 'PDF', resolution=100.0)
        send_email_thread(email,pdf_buffer)
        messages.success(request,"Ticket has been sent to your registered email")
        return redirect('profile')
    messages.warning(request,"Something went wrong")
    return redirect('profile')