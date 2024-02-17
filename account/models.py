from datetime import datetime, timedelta
from django.db import models
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username=None
    phone=models.CharField(max_length=10,unique=True)
    _pass =models.OneToOneField(to='Passes',on_delete=models.SET_NULL,null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD='phone'
    REQUIRED_FEILDS=[]
    def __str__(self):
        return str(self.id)
    


class Profile(models.Model):
    user = models.OneToOneField(to='User',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    email=models.EmailField(max_length=200)
    dob=models.DateField(null=True)
    sem=models.IntegerField(null=True)
    college=models.CharField(max_length=200)
    address=models.CharField(max_length=200)

# class Wallet(models.Model):
#     # userid=models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.OneToOneField(to='User',on_delete=models.CASCADE)
#     walletid=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
#     balance = models.IntegerField(default=0)
#     def __str__(self) -> str:
#         return self.user.email

class Passes(models.Model):
    phone = models.CharField(max_length=10,unique=True,null=False,blank=False)
    technical1 =models.ForeignKey(to="ticket.Events",on_delete=models.SET_NULL,null=True,blank=True,related_name="Technical_Event_1")
    technical2 =models.ForeignKey(to="ticket.Events",on_delete=models.SET_NULL,null=True,blank=True,related_name="Technical_Event_2")
    splash =models.ForeignKey(to="ticket.Events",on_delete=models.SET_NULL,null=True,blank=True,related_name="Splash_Event")
    
    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = 'Pass'
        verbose_name_plural = 'Passes'
        
class OTP(models.Model):
    user = models.OneToOneField(to="User",on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(null=True,blank=True)
    expiry = models.DateTimeField(default=datetime.now()+timedelta(minutes=10))