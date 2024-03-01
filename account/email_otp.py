from threading import Thread
import boto3
from botocore.exceptions import ClientError
from requests import request
from config import settings
from collections.abc import Mapping
from .models import User
def send_otp(email,otp):
    SENDER = settings.Email
    RECIPIENT = email
    AWS_REGION = "ap-south-1"
    user=User.objects.get(email=email)
    name=user.first_name+" "+user.last_name
    SUBJECT = "JECRC Renaissance OTP: Your Access Code"
    BODY_TEXT = (f"Hi {name}, Your one-time password (OTP) for accessing the Renaissance is: {otp} This OTP is valid for 10 minutes.Please do not share it with anyone. We hope you have a great time at Renaissance!")
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1></h1>
    <p>Hi {name},<br> Your one-time password (OTP) for accessing the Renaissance is: <b>{otp}</b> . <br> This OTP is valid for 10 minutes.<br> Please do not share it with anyone. <br> We hope you have a great time at Renaissance!<br></p>
    </body>
    </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',
                          region_name=AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )	
    except ClientError as e:
        print(e.response['Error']['Message'])
    except Exception as e:
        print(e)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
def send_otp_thread(email, otp):
    t = Thread(target=send_otp, args=(email, otp))
    t.start()