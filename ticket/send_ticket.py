import os
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from config import settings
from ticket.models import Ticket

def send_email_with_attachment(email, img_data):
    # Initialize SES client
    ses_client = boto3.client('ses', region_name='ap-south-1',aws_access_key_id="AKIA3WO4ZFTK7JW4U6XT",aws_secret_access_key="qOabbapjbKMcPbxPh7HvflvV7ikMNSGktD80Dtf4")  # Replace with your desired region
    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = 'Your ticket for Renissance 2k24'
    message['From'] = settings.Email
    message['To'] = email

    # Add HTML content (optional)
    html_content = MIMEText('<p>Hello, this is your email content.</p>', 'html')
    message.attach(html_content)

    # Attach the image
    attachment = MIMEApplication(img_data)
    attachment.add_header('Content-Disposition', 'attachment', filename='Ticket.png')
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

# Example usage
recipient_email = 'recipient@example.com'
# Replace with your actual image data (bytes)
image_bytes = b'\x89PNG\r\n\x1a\n...'
send_email_with_attachment(recipient_email, image_bytes)
