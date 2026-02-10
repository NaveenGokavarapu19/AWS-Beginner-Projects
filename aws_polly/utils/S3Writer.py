import os 

class S3Writer():
    def __init__(self,s3_resource, bucket_name):
        print(f"Initializing S3Writer with bucket name: {bucket_name}")
        self.s3_resource = s3_resource
        self.bucket_name = bucket_name

    
    def return_bucket_object(self):
        return self.s3_resource.Bucket(self.bucket_name)
    
    def download_object(self,s3_object_prefix,dowload_path):
        s3_bucket_object = self.return_bucket_object()
        s3_bucket_object.download_file(Key=s3_object_prefix,Filename=dowload_path)

    def put_object(self,file_path,s3_file_upload_path):
        s3_bucket_object = self.return_bucket_object()
        file_object = open(file_path,'rb') 
        s3_bucket_object.put_object(Key=s3_file_upload_path,Body=file_object)
        file_object.close()


