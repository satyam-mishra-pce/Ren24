import boto3
from botocore.credentials import InstanceMetadataProvider, InstanceMetadataFetcher

provider = InstanceMetadataProvider(
    iam_role_fetcher=InstanceMetadataFetcher(timeout=1000, num_attempts=2)
)
creds = provider.load().get_frozen_credentials()


def getParameter(param_name):
    """
    This function reads a secure parameter from AWS' SSM service.
    The request must be passed a valid parameter name, as well as
    temporary credentials which can be used to access the parameter.
    The parameter's value is returned.
    """
    # Create the SSM Client
    # ssm = boto3.client('ssm',
    #     region_name='ap-south-1',
    #     aws_access_key_id = "AKIA3WO4ZFTK7JW4U6XT",
    # aws_secret_access_key = "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"
    # )

    ssm = boto3.client(
        "ssm",
        region_name="ap-south-1",
        aws_access_key_id=creds.access_key,
        aws_secret_access_key=creds.secret_key,
        aws_session_token=creds.token,
    )

    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[
            param_name,
        ],
        # WithDecryption=True
    )

    # Store the credentials in a variable
    credentials = response["Parameters"][0]["Value"]

    return credentials
