import boto3
from botocore.exceptions import ClientError
from requests import request
from config import settings
from collections.abc import Mapping
# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
def send_otp(email,otp):
    SENDER = settings.Email

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = "OTP for Renaissance 2k24"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (f"Your OTP is : {otp}")
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>OTP for Renaissance 2k24</h1>
    <p>Your OTP is : {otp} </p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION,aws_access_key_id="AKIA3WO4ZFTK7JW4U6XT",aws_secret_access_key="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")

    # Try to send the email.
    try:
        #Provide the contents of the email.
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
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])