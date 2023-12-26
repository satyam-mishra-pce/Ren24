from datetime import timedelta
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    def __str__(self):
        return str(self.userid)
    userid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username=None
    email=models.EmailField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    
    USERNAME_FIELD='id'
    


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
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)