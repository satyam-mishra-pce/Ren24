from threading import Thread
import boto3
from botocore.exceptions import ClientError
from requests import request
from config import settings
from collections.abc import Mapping
def send_otp(email,otp):
    SENDER = settings.Email
    RECIPIENT = email
    AWS_REGION = "ap-south-1"
    SUBJECT = "OTP for Renaissance 2k24"
    BODY_TEXT = (f"Your OTP is : {otp}")
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>OTP for Renaissance 2k24</h1>
    <p>Your OTP is : {otp} </p>
    </body>
    </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION,aws_access_key_id="AKIA3WO4ZFTK7JW4U6XT",aws_secret_access_key="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")
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