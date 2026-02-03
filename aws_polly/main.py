from utils import aws_boto3_client

def lambda_handler(event, context):
    try:
        polly_client = aws_boto3_client.return_client('polly',region_name='us-east-1')
        response = polly_client.describe_voices(
            Engine='standard',
            LanguageCode='en-IN'
        )
        print(response)
    except Exception as e:
        print(f"Error: {e=}")
