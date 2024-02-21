from django.db import models
from account.models import User
from ticket.models import Events

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Events,on_delete=models.CASCADE)

class Transaction(models.Model):
    def __str__(self):
        return str(self.id)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=200)
    amount=models.IntegerField(null=True)
    # type=models.CharField(max_length=6,choices=_types,blank=False)
    is_paid = models.BooleanField(default=False)