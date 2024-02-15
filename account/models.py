from datetime import timedelta
from django.db import models
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username=None
    id = models.BigAutoField(primary_key=True)
    phone=models.CharField(max_length=10)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    # is_verified=models.BooleanField(default=False,editable=True)
    
    objects = UserManager()
    
    USERNAME_FIELD='id'
    REQUIRED_FEILDS=['email']
    def __str__(self):
        return str(self.userid)
    


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
    phone = models.CharField(max_length=10,null=False,blank=False)
    technical1 =models.ForeignKey(to="ticket.Events",on_delete=models.CASCADE,related_name="Technical_Event_1")
    technical2 =models.ForeignKey(to="ticket.Events",on_delete=models.CASCADE,related_name="Technical_Event_2")
    Splash =models.ForeignKey(to="ticket.Events",on_delete=models.CASCADE,related_name="Splash_Event")