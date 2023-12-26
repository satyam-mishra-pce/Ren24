from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render,redirect
from config import settings
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login, logout,authenticate
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# Create your views here.

def home(request):
    return render(request,'index.html')


def register(request):
    """Create a new user account and send a confirmation email."""
    # check if the request is a POST method
    if request.method == "POST":
        # get the input data from the request
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # validate the input data
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        # create a new user object with the input data
        myuser = User.objects.create_user(email=email, first_name=fname,last_name=lname,is_active=False)
        myuser.save()
        
        # return a success message
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        #Welcome Email
        subject="Welcome to Ren2024"
        message="Hello " + myuser.first_name + "!! \n" +"Welcome to Renaissance 2024 website. \n Thank you for your valuable registration. \n We have also send to a confirmation mail please verify yor email address to get started. \n Thanks regards, \n JECRC "
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[myuser.email]
        send_mail(subject,message,from_email,recipient_list,fail_silently=True)
        
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @Ren2024"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('signin')
    
    # if the request is not a POST method, render a template with a form
    else:
        return render(request, 'register.html')
    

def signin(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        user=User.objects.get(email=email)
        print(user,password)
        if user:
            if (user.is_active==True):
                myuser=authenticate(id=user.id, password=password)
                print(myuser)
                if myuser is not None:
                    login(request,user)
                    messages.success(request,"Logged IN Sucessfully")
                    # request.session['fname'] = user[0].first_name
                    # request.session['is_verified'] = user[0].is_verified
                    # request.session['id'] = user[0].pk
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

def activate(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser= None
        
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        Wallet.objects.create(userid=myuser)
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    
    else:
        return render(request, 'activation_failed.html')