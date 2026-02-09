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

    def put_object(self,file_path,file_name,key=None):
        s3_bucket_object = self.return_bucket_object()
        resource_path = os.path.join(file_path,file_name)
        s3_bucket_path = os.path.join(s3_file_path,file_name)
        file_object = open(resource_path,'rb') 
        s3_bucket_object.put_object(Key=s3_bucket_path,Body=file_object)
        print(f"Object {file_name} put in bucket {self.bucket_name}")
        file_object.close()


