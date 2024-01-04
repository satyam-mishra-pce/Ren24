import uuid
from django.db import models
from account.models import User
# Create your models here.

_types = [
    ('debit',"Debit"),
    ('credit',"Credit"),
]

_eventTypes = [
    ('cultural',"Cultural"),
    ('splash',"Splash"),
    ('tech',"Technical")
]

class Transaction(models.Model):
    def __str__(self):
        return str(self.id)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=200)
    amount=models.IntegerField(null=True)
    type=models.CharField(max_length=6,choices=_types,blank=False)
    is_paid = models.BooleanField(default=False)
    
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=8,choices=_eventTypes)
    description = models.TextField(max_length=500)
    cost = models.PositiveIntegerField(default=0)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # qr_code = models.ImageField(upload_to='passes/qr', blank=True)

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):

    #     qr_image = qrcode.make(str(self.id))
    #     style = Image.new("RGB", (600,600), "red")
    #     style.paste(qr_image)
    #     file_path = os.path.join(f"{self.user}_qr.png")
    #     stream = BytesIO()
    #     style.save(stream, "PNG")
    #     self.qr_code.save(file_path, File(stream), save=False)
    #     style.close()
    #     super().save(*args, **kwargs)