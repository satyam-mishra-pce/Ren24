import qrcode
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

from ticket.models import Ticket

def generate_ticket(ticket_id)->bytes:
    ticket = Ticket.objects.get(id=ticket_id)
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(ticket_id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create a blank image with white background
    ticket_img = Image.new("RGB", (900, 300), "white")
    draw = ImageDraw.Draw(ticket_img)

    # Paste the QR code onto the image
    qr_img = qr_img.resize((280, 280))  # Resize QR code image if necessary
    ticket_img.paste(qr_img, (10, 10))
    font_name = "/usr/share/fonts/truetype/dejavu/DejaVuMathTeXGyre.ttf"

    # Draw user's name and date onto the image
    font = ImageFont.truetype(font_name, 32)  # Use a suitable font
    font_medium = ImageFont.truetype(font_name, 24)  # Use a suitable font
    font_small = ImageFont.truetype(font_name, 16)  # Use a suitable font
    draw.text((350, 25), f"Booking Id: {ticket.id}", fill="grey", font=font_small)
    draw.text((350, 70), f"{ticket.user.first_name} {ticket.user.last_name}", fill="black", font=font)
    draw.text((350, 120),ticket.event.name.upper(), fill="black", font=font)
    draw.text((350, 170),f"Venue : {ticket.event.venue}", fill="grey", font=font_medium)
    draw.text((350, 220),ticket.event.time.strftime("%-I:%M %p"), fill="black", font=font_medium)
    draw.text((600, 220),ticket.event.date.strftime("%a, %d %b, %Y"), fill="black", font=font_medium)

    # Save the image to a BytesIO buffer
    img_io = BytesIO()
    ticket_img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io.getvalue()
