import uuid
from django.db import models
from account.models import User
# Create your models here.

# _types = [
#     ('debit',"Debit"),
#     ('credit',"Credit"),
# ]

_eventTypes = [
    ('cultural',"Cultural"),
    ('splash',"Splash"),
    ('tech',"Technical")
]


    
class Events(models.Model):
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    type = models.CharField(max_length=8,choices=_eventTypes)
    description = models.TextField(max_length=500)
    amount = models.PositiveIntegerField(default=0)
    includedInPass = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='events/')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

class Ticket(models.Model):
    id= models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    used = models.BooleanField(default=False)
    # qr_code = models.ImageField(upload_to='passes/qr', blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

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
    
# class CustomTicket(models.Model):
#     id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
#     event = models.ForeignKey(Events, on_delete=models.CASCADE)
#     amount = models.PositiveIntegerField(default=0)
#     comment = models.TextField(null=True,blank=True)
#     is_paid = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=False, blank=True,null=True)
#     # qr_code = models.ImageField(upload_to='passes/qr', blank=True)

#     def __str__(self):
#         return str(self.id)