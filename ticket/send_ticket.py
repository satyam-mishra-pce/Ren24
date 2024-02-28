# import base64
# import boto3
# from botocore.exceptions import ClientError
# from requests import request
# from config import settings
# from collections.abc import Mapping

# from ticket.functions import generate_ticket

# from .models import Ticket

# # Replace sender@example.com with your "From" address.
# # This address must be verified with Amazon SES.
# def send_ticket(email ,ticket_id,img_data):
#     SENDER = settings.Email
    
#     # Replace recipient@example.com with a "To" address. If your account
#     # is still in the sandbox, this address must be verified.
#     RECIPIENT = email

#     # Specify a configuration set. If you do not want to use a configuration
#     # set, comment the following variable, and the
#     # ConfigurationSetName=CONFIGURATION_SET argument below.
#     CONFIGURATION_SET = "ConfigSet"

#     # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
#     AWS_REGION = "ap-south-1"

#     # The subject line for the email.
    
#     ticket_obj = Ticket.objects.get(id=ticket_id)
#     SUBJECT = f"Your Ticket for {ticket_obj.event.name}"

#     # The email body for recipients with non-HTML email clients.
#     BODY_TEXT = ("Please see attached")

#     # The HTML body of the email.
#     BODY_HTML = f"""<html>
#         <head></head>
#         <body>
#             <h1></h1>
#             <p>Please see attached file</p>
#         </body>
#     </html>
#     """

#     # The character encoding for the email.
#     CHARSET = "UTF-8"
#     # Create a new SES resource and specify a region.
#     client = boto3.client('ses', region_name=AWS_REGION,
#                           aws_access_key_id="AKIA3WO4ZFTK7JW4U6XT",
#                           aws_secret_access_key="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")

#     try:
#         # img_data=generate_ticket(ticket_id)

#         # Provide the contents of the email, including the attachment
#         response = client.send_email(
#             Destination={
#                 'ToAddresses': [
#                     RECIPIENT,
#                 ],
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': CHARSET,
#                         'Data': BODY_HTML,
#                     },
#                     'Text': {
#                         'Charset': CHARSET,
#                         'Data': BODY_TEXT,
#                     },
#                 },
#                 'Subject': {
#                     'Charset': CHARSET,
#                     'Data': SUBJECT,
#                 },
#             },
#             # If you are not using a configuration set, comment or delete the
#             # following line
#             # ConfigurationSetName=CONFIGURATION_SET,
#             Attachments=[
#                 {
#                     'Content': img_data,
#                     'Headers': [
#                         {'Name': 'Content-Type', 'Value': 'image/png'},
#                         {'Name': 'Content-Disposition', 'Value': 'attachment; filename="Ticket.png"'}
#                     ]
#                 }
#             ],
#             Source=SENDER,
#             Destinations=email,
#         )
#         print("Email sent! Message ID:", response['MessageId'])
#     except ClientError as e:
#         print(e.response['Error']['Message'])

import base64
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from config import settings  # Import configuration details (email, credentials, etc.)
from ticket.functions import generate_ticket  # Import ticket generation function

from .models import Ticket  # Import relevant model if applicable


def send_ticket(email, ticket_id):
    """
    Sends an email with the generated ticket image as an attachment.

    Args:
        email (str): Email address of the recipient.
        ticket_id (int): ID of the ticket.

    Returns:
        None
    """

    message = MIMEMultipart()
    message['Subject'] = 'Ticket'
    message['From'] = settings.Email
    message['To'] = email

    # Message body
    message.preamble = 'Multipart message.\n'
    body = MIMEText('Howdy -- here is the data from last week.')
    message.attach(body)

    # Attachment
    img_data = generate_ticket(ticket_id)

    # Ensure data is in bytes format (no need for conversion if already bytes)
    if not isinstance(img_data, bytes):
        img_data_as_bytes = bytes(img_data, 'utf-8')
    else:
        img_data_as_bytes = img_data

    attachment = MIMEApplication(img_data_as_bytes)
    attachment.add_header('Content-Disposition', 'attachment; filename="Ticket.png"')

    # **Debugging Tips:**
    # 1. Print the content type and headers of the attachment:
    print("Attachment content type:", attachment.get_content_type())
    print("Attachment headers:", attachment.headers)

    # 2. Check if the attachment is actually attached to the message:
    print("Attached parts:", message.get_payload())

    # Attach the image to the message
    message.attach(attachment)

    # Connect to SES and send the email
    client = boto3.client(
        'ses',
        region_name='ap-south-1',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    try:
        response = client.send_email(
            Source=message['From'],
            Destination={
                'ToAddresses': [message['To']]
            },
            Message={
                'Body': {
                    'Text': {
                        'Data': body.as_string(),
                        'Charset': 'UTF-8'
                    }
                },
                'Subject': {
                    'Data': message['Subject'],
                    'Charset': 'UTF-8'
                }
            }
        )
        print(f"Email sent successfully. Response: {response}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage (replace with actual values)
# ticket_id = 1
# send_ticket(recipient_email, ticket_id)


# Example usage (replace with actual values)
# ticket_id = 1
# send_ticket(recipient_email, ticket_id)

# Example usage (replace with actual values)
# ticket_id = 1
# send_ticket(recipient_email, ticket_id)



# Call the function (example usage)
# ticket_id = 1  # Replace with actual ticket ID
# send_ticket(recipient_email, ticket_id)  # Replace with recipient email
