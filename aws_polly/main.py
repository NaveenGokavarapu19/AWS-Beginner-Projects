from utils import aws_boto3_client

def main():
    try:
        polly_client = aws_boto3_client.return_client('polly',region_name='us-east-1',profile_name='superadmin')
        response = polly_client.describe_voices(
            Engine='standard',
            LanguageCode='en-IN'
        )
        print(response)
    except Exception as e:
        print(f"Error: {e=}")

main()