from django.db import models
from account.models import User
from ticket.models import Events

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Events,on_delete=models.CASCADE)
