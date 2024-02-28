from pathlib import Path
from os import path
import qrcode
# from django.http import HttpResponse
from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

from ticket.models import Ticket

def generate_ticket(ticket_id)->bytes:
    BASE_DIR = Path(__file__).resolve().parent
    ticket = Ticket.objects.get(id=ticket_id)
    # Generate QR code
    logo = Image.open(path.join(BASE_DIR,'assets','Ren logo.png'))
    logo = logo.resize((70, 70))
    qr = qrcode.QRCode(
        version=1, 
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        )
    qr.add_data(ticket_id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(0,0,0), back_color="transparent").convert('RGBA')
    qr_img = qr_img.resize((270, 270))  # Resize QR code image if necessary
    pos = (100,100)
    qr_img.paste(logo, pos,logo)

    # Create a blank image with white background
    # ticket_img = Image.new("RGB", (900, 300), "white")
    ticket_img = Image.open(path.join(BASE_DIR,'assets','ticket-01.png'),'r')
    ticket_img = ticket_img.resize((900,300))
    draw = ImageDraw.Draw(ticket_img)

    # Paste the QR code onto the image
    ticket_img.paste(qr_img, (15, 15),qr_img)
    font_name = path.join(BASE_DIR,'assets','Ubuntu_Mono','UbuntuMono-Regular.ttf')

    # Draw user's name and date onto the image
    font = ImageFont.truetype(font_name, 32)  # Use a suitable font
    font_medium = ImageFont.truetype(font_name, 24)  # Use a suitable font
    font_small = ImageFont.truetype(font_name, 16)  # Use a suitable font
    draw.text((350, 25), f"Booking Id: {ticket.id}", fill="white", font=font_small)
    draw.text((350, 70), f"{ticket.user.first_name} {ticket.user.last_name}", fill="black", font=font)
    draw.text((350, 120),ticket.event.name.upper(), fill="black", font=font)
    draw.text((350, 170),f"Venue : {ticket.event.venue}", fill="white", font=font_medium)
    draw.text((350, 220),ticket.event.time.strftime("%-I:%M %p"), fill="black", font=font_medium)
    draw.text((600, 220),ticket.event.date.strftime("%a, %d %b, %Y"), fill="black", font=font_medium)

    # Save the image to a BytesIO buffer
    img_io = BytesIO()
    ticket_img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io.getvalue()
