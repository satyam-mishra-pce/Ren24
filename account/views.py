# from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render,redirect
# from account.forms import ProfileForm
from config import settings
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
            return render(request, 'register.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return render(request, 'register.html')
        
        myuser = User.objects.create_user(phone=phone, 
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
        
        # #Welcome Email
        # subject="Welcome to Ren2024"
        # message="Hello " + myuser.first_name + "!! \n" +"Welcome to Renaissance 2024 website. \n Thank you for your valuable registration. \n We have also send to a confirmation mail please verify yor email address to get started. \n Thanks regards, \n JECRC "
        # from_email=settings.EMAIL_HOST_USER
        # recipient_list=[myuser.email]
        # send_mail(subject,message,from_email,recipient_list,fail_silently=True)
        
        
        # # Email Address Confirmation Email
        # current_site = get_current_site(request)
        # email_subject = "Confirm your Email @Ren2024"
        # message2 = render_to_string('email_confirmation.html',{
        #     'name': myuser.first_name,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        # })
        # email = EmailMessage(
        # email_subject,
        # message2,
        # settings.EMAIL_HOST_USER,
        # [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()
        return redirect('verify')
    
    # if the request is not a POST method, render a template with a form
    else:
        return render(request, 'register.html')
    
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
                print(myuser,password,phone)
                if myuser is not None:
                    login(request,user)
                    messages.success(request,"Logged IN Sucessfully")
                    return redirect('home')
                else:
                    # return Response({"message": "Incorrect password!"}, status=400)      
                    messages.error(request, "Incorrect Password")
                    return render(request,"login.html")
            else:
                # return Response({"message": "User is not verified!"}, status=200)
                messages.error(request, "User not verified")
                return render(request,"login.html")
        else:
            # return Response({"message": "User does not exist!"}, status=400)
            messages.error(request, "User does not exist")
            return render(request,"login.html")
    else:
        return render(request,"login.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully")
    return redirect('home')

# def activate(request, uidb64, token):
#     try:
#         uid=force_str(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         myuser= None
        
#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active=True
#         myuser.save()
#         # Wallet.objects.create(user=myuser)
#         login(request,myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
    
#     else:
#         return render(request, 'activation_failed.html')
    
    
@login_required
def profile_view(request):
    if request.method == 'GET':
        # get the current user's profile or create a new one
        profile, created = Profile.objects.get_or_create(user=request.user)
        # render the template with the profile data
        tickets = Ticket.objects.filter(user=request.user)
        context = {
            'profile':profile,
            'tickets':tickets
        }
        return render(request, 'profile.html',context)
    elif request.method == 'POST':
        return 
