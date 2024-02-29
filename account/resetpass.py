from .email_otp import send_otp
import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
import pytz
from account.models import OTP, User
from account.views import generateOTP


def resendOTP(request):
    myuser=User.objects.get(id=request.session.get("id"))
    otp_obj= OTP.objects.get(user=myuser)
    otp_obj.otp = generateOTP()
    otp_obj.created = datetime.datetime.now(pytz.UTC)
    otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
    otp_obj.save()
    # TODO: Send OTP to phone number
    print("\n")
    print("\n")
    print(otp_obj.otp)
    print("\n")
    print("\n")
    otp_obj.save()
    send_otp(myuser.email,otp_obj.otp)
    return redirect('resetpass_verify')

def verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.get(id=request.session.get("id"))  # Use get() to avoid KeyError
        otp_obj = OTP.objects.filter(user=user).first()  # Use filter() to handle None case
        if otp_obj:
            check_otp=str(otp_obj.otp)
            if otp==check_otp:  
                if datetime.datetime.now(pytz.UTC) > otp_obj.expire:
                    messages.warning(request, "OTP has expired")
                    return redirect('login')
                if otp_obj.user.is_active:
                    return render(request, 'newpass.html')
                
            else:
                print(type(check_otp))
                print(type(otp))
                messages.error(request, 'Wrong OTP')
        else:
            messages.error(request, 'Invalid OTP or user not found')  # Handle None case
        return redirect('verify')
    else:
        return render(request, 'resetpass_verify.html')


    
def forgotpassword(request):
    if request.method=="POST" and 'email' in request.POST:
        email=request.POST['email']
        myuser=User.objects.filter(email=email).first()
        if not myuser:
            messages.error(request,"No account associated with this Email.")
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
        id=User.objects.filter(email=email).values('id').first()["id"]
        request.session['id']=id
        return redirect('resetpass_verify')
    elif request.method == 'POST' and 'pass1' in request.POST:
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        id=request.session.get('id')
        if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return render(request,'newpass.html')
        
        myuser = User.objects.get(id=id)
        myuser.set_password(pass1)
        myuser.save()
        return redirect('home')
    else:
        return  render(request,'entermobile.html')

def newpass(request):
    if request.method=='POST':
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        email=request.session.get('email')
        if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('home')
        
        myuser = User.objects.get(email).first()
        myuser.update(password=pass1)
        myuser.save()
        return redirect('login')