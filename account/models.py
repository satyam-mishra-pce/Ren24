from datetime import timedelta
import datetime
import uuid
from django.db import models
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username=None
    id = models.BigAutoField(primary_key=True)
    userid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email=models.EmailField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False,editable=True)
    
    objects = UserManager()
    
    USERNAME_FIELD='id'
    REQUIRED_FEILDS=['email']
    def __str__(self):
        return str(self.userid)
    


class Profile(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    phone=models.CharField(max_length=10)
    dob=models.DateField()
    sem=models.IntegerField()
    college=models.CharField(max_length=200)
    address=models.CharField(max_length=200)

class Wallet(models.Model):
    userid=models.ForeignKey(User, on_delete=models.CASCADE)
    walletid=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    balance = models.IntegerField(default=0)