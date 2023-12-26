from datetime import timedelta
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return str(self.userid)
    username=models.CharField(unique=True,max_length=100,null=True)
    userid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email=models.EmailField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    
    USERNAME_FIELD='username'
    REQUIRED_FEILDS=[]
    


class Profile(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    image=image = models.ImageField(upload_to='user_images/')
    phone=models.IntegerField()
    dob=models.DateField()
    sem=models.IntegerField()
    college=models.CharField(max_length=200)
    address=models.CharField(max_length=200)

class Wallet(models.Model):
    userid=models.ForeignKey(User, on_delete=models.CASCADE)
    walletid=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    balance = models.IntegerField(default=0)