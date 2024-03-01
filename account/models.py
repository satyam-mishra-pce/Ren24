from datetime import datetime, timedelta
import uuid
from django.db import models
import pytz
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

_genders = [("m","Male"),
           ("f","Female"),
           ("o","Other")]

genders = {
    'Male':'m',
    'Female':'f',
    'Other':'o',
}

# Create your models here.
class User(AbstractUser):
    username=None
    email=models.EmailField(max_length=200,unique=True)
    _pass =models.OneToOneField(to='Passes',on_delete=models.SET_NULL,null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD='id'
    REQUIRED_FEILDS=[]
    def __str__(self):
        return self.email
    


class Profile(models.Model):
    user = models.OneToOneField(to='User',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    phone=models.CharField(max_length=10,unique=True,null=True)
    gender=models.CharField(max_length=1,null=True,blank=True,choices=_genders)
    rollno=models.CharField(max_length=16,unique=True,null=True)
    dob=models.DateField(null=True)
    college=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.email

# class Wallet(models.Model):
#     # userid=models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.OneToOneField(to='User',on_delete=models.CASCADE)
#     walletid=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
#     balance = models.IntegerField(default=0)
#     def __str__(self) -> str:
#         return self.user.email

class Passes(models.Model):
    psid=models.UUIDField(default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=200,unique=True,null=False,blank=False)
    technical =models.ForeignKey(to="ticket.Events",on_delete=models.SET_NULL,null=True,blank=True,related_name="Technical_Event")
    splash =models.ForeignKey(to="ticket.Events",on_delete=models.SET_NULL,null=True,blank=True,related_name="Splash_Event")
    day1=models.BooleanField(default=False)
    day2=models.BooleanField(default=False)
    day3=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Pass'
        verbose_name_plural = 'Passes'
        
class OTP(models.Model):
    user = models.OneToOneField(to="User",on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(null=True,blank=True)
    created = models.DateTimeField(default=datetime.now(pytz.UTC))
    expire=models.DateTimeField(default=(datetime.now(pytz.UTC)+timedelta(seconds=30)))
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTP(s)'