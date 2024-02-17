import qrcode
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def generate_ticket(request, format):
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    data = "User: John Doe\nDate: 2024-02-16"  # Example data
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Render ticket
    user_name = "John Doe"
    date = "2024-02-16"

    if format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

        # Generate PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "E-Ticket")
        p.drawString(100, 730, f"User: {user_name}")
        p.drawString(100, 710, f"Date: {date}")
        p.drawImage(BytesIO(qr_img.tobytes()), 100, 600, width=200, height=200)
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
    elif format == 'png':
        # Generate PNG
        img_io = BytesIO()
        qr_img.save(img_io, format='PNG')
        img_io.seek(0)
        response = HttpResponse(img_io.getvalue(), content_type='image/png')
    else:
        # Handle unsupported format
        return HttpResponse("Unsupported format")

    return response
