from utils import aws_boto3_client
from utils.S3Writer import S3Writer
import os
from zipfile import ZipFile



BucketName = os.environ.get('BUCKET_NAME')
s3_main_path = os.environ.get('S3_MAIN_PATH')
s3_prefix = os.environ.get('S3_PREFIX') # sub path where the file will be stored in s3
main_directory = '/tmp' # where all the resources are present in lambda function
resource_file_path = 'aws_polly/resources/text_files' # the path where the text file is present.
file_name = 'story.txt' 
download_path = 'aws_polly/resources/downloads/text_files'
result_path = 'aws_polly/resources/output_files'
zip_path = 'aws_polly/resources/zip_files'




def replace_text_in_file_helper(text,old_text,new_text):
    return text.replace(old_text,new_text)

def create_path_helper(*args):
    return os.path.join(*args)


def zip_file(file_path,file_name,zip_file_path):
    resource_path = os.path.join(file_path,file_name)
    new_file_name = replace_text_in_file_helper(file_name,'.mp3','.zip')
    with ZipFile(f"{new_file_name}",'w') as zip_object:
        zip_object.write(resource_path)

def read_file(file_path,file_name):
    resource_path = create_path_helper(file_path,file_name)
    with open(resource_path,'r') as file_object:
        return file_object.read()
    
def write_file(file_path,file_name,object):
    resource_path = create_path_helper(file_path,file_name)
    with open(resource_path,'wb') as file_object:
        file_object.write(object)


def lambda_handler(event, context):
    try:
        s3_resource = aws_boto3_client.return_resource('s3',region_name='us-east-1')
        s3_writer = S3Writer(s3_resource,BucketName)
        s3_object_prefix_download = create_path_helper(s3_main_path,s3_prefix,download_path,file_name)
        # file_path = create_path_helper(main_directory,resource_file_path,file_name)
        download_path = create_path_helper(main_directory,download_path,file_name)
        s3_writer.download_object(s3_object_prefix=s3_object_prefix_download,)
        text = read_file(download_path, file_name)
        polly_client = aws_boto3_client.return_client('polly',region_name='us-east-1',profile_name=profile_name)
        response = polly_client.synthesize_speech(
            OutputFormat='mp3',
            Text=text,
            VoiceId='Aditi'
        )
        audio_stream = response['AudioStream'].read()
        write_file(result_path,replace_text_in_file_helper(file_name,'.txt','.mp3'),audio_stream)
        zip_file(result_path,replace_text_in_file_helper(file_name,'.txt','.mp3'),zip_path)
        # s3_writer.put_object(file_path=file_path,file_name=file_name,s3_file_path=s3_file_path,key=s3_object_prefix)
        
    except Exception as e:
        print(f"Error: {e=}")


lambda_handler(None,None)