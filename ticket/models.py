from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io
from os import path
from pathlib import Path
from threading import Thread
import uuid
from django.db import models
import qrcode
from account.models import User
from config import settings
import boto3
from PIL import Image,ImageDraw,ImageFont

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
    description = models.TextField(max_length=1000,null=True,blank=True)
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
    created = models.DateTimeField(auto_now_add=True, blank=True,null=True)
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
    
class CustomTicket(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=200)
    phone_no = models.CharField(max_length=13, unique=True)
    used = models.BooleanField(default=False)
    # amount = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        ticket = self.generate_customticket()
        image_buffer = io.BytesIO(ticket)
        image=Image.open(image_buffer)
        img_rgb=image.convert('RGB')
        pdf_buffer = io.BytesIO()
        img_rgb.save(pdf_buffer, 'PDF', resolution=100.0)
        send_custom_email_thread(self.email,pdf_buffer)
        print(f"Custom ticket saved {self.id}")
        super().save(*args, **kwargs)
    
    def generate_customticket(self)->bytes:
        BASE_DIR = Path(__file__).resolve().parent
        # Generate QR code
        logo = Image.open(path.join(BASE_DIR,'assets','Ren logo.png'))
        logo = logo.resize((70, 70))
        qr = qrcode.QRCode(
            version=1, 
            border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            )
        qr.add_data(f"{settings.BASE_URL}/custom/{self.id}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=(0,0,0), back_color="transparent").convert('RGBA')
        qr_img = qr_img.resize((270, 270))  # Resize QR code image if necessary
        pos = (100,100)
        qr_img.paste(logo, pos,logo)

        # Create a blank image with white background
        # ticket_img = Image.new("RGB", (900, 300), "white")
        ticket_img = Image.open(path.join(BASE_DIR,'assets','ticket-02-01.png'),'r')
        ticket_img = ticket_img.resize((900,300))
        draw = ImageDraw.Draw(ticket_img)

        # Paste the QR code onto the image
        ticket_img.paste(qr_img, (15, 15),qr_img)
        font_name = path.join(BASE_DIR,'assets','Ubuntu_Mono','UbuntuMono-Regular.ttf')

        # Draw user's name and date onto the image
        font = ImageFont.truetype(font_name, 32)  # Use a suitable font
        font_medium = ImageFont.truetype(font_name, 24)  # Use a suitable font
        font_small = ImageFont.truetype(font_name, 16)  # Use a suitable font
        draw.text((350, 25), f"Booking Id: {self.id}", fill="black", font=font_small)
        draw.text((350, 70), f"{self.name} ", fill="black", font=font)
        draw.text((350, 115),f"{self.email}", fill="black", font=font_medium)
        draw.text((350, 150),f"{self.phone_no}", fill="black", font=font_medium)
        draw.text((350, 200),self.event.name.upper(), fill="black", font=font_medium)
        draw.text((600, 200),self.event.venue, fill="black", font=font_medium)
        draw.text((350, 240),self.event.time.strftime("%-I:%M %p"), fill="black", font=font_medium)
        draw.text((600, 240),self.event.date.strftime("%a, %d %b, %Y"), fill="black", font=font_medium)
    

        # Save the image to a BytesIO buffer
        img_io = io.BytesIO()
        ticket_img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io.getvalue()
        
def send_custom_email_with_attachment(email,pdf_buffer):
    # Initialize SES client
    ses_client = boto3.client('ses', 
                              region_name='ap-south-1', 
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                              )  # Replace with your desired region and credentials
    
    name_obj=CustomTicket.objects.get(email=email)
    name=name_obj.name
    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = f'Your Ticket for Renaissance!'
    message['From'] = settings.Email
    message['To'] = email

    # Add HTML content (optional)
    html_content = MIMEText(f'<p>Hi {name}, <br>Thank you for registering for Renaissance!,</br> <br></br> <br>Your QR ticket is attached to this email.</br> <br> </br> <br>Please present this ticket at the event entrance for scanning. We look forward to seeing you there!</br> <br> </br> <br> </br> <br> Thanks regards,</br> <br> JECRC Renaissance</br></p>', 'html')
    message.attach(html_content)

    # Attach the image
    attachment = MIMEApplication(pdf_buffer.getvalue())
    attachment.add_header('Content-Disposition', 'attachment', filename='Ticket.pdf')
    message.attach(attachment)

    # Send the email
    try:
        response = ses_client.send_raw_email(
            Source=message['From'],
            Destinations=[message['To']],
            RawMessage={'Data': message.as_string()}
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def send_custom_email_thread(email,img_data):
    t = Thread(target=send_custom_email_with_attachment, args=(email, img_data))
    t.start()