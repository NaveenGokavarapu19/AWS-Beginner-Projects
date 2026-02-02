import boto3

def return_client(service_name,region_name=None,profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    if region_name:
        return session.client(service_name=service_name,region_name=region_name)
    return session.client(service_name,profile_name=profile_name)