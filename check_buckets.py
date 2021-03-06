from datetime import date
from datetime import datetime, timedelta
import requests
import json
import boto3
from botocore.client import Config
import os


print(requests.certs.where())

secrets_from_env = False
download_all = True

if secrets_from_env == True:
    config = { 'api_key': os.getenv('API_KEY'),
            'directory': os.getenv('DIRECTORY'),
            'hosts': {'local': {'accessKey': os.getenv('S3_ACCESSKEY'),
            'api': os.getenv('S3_API'), 'lookup': os.getenv('S3_LOOKUP'), 
            'secretKey': os.getenv('S3_SECRETKEY'), 'url': os.getenv('S3_URL')}} }
else:
    with open('config.json', 'r') as f:
        config = json.load(f)

accessKey = config['hosts']['local']['accessKey']
api = config['hosts']['local']['api']
lookup = config['hosts']['local']['lookup']
secretKey = config['hosts']['local']['secretKey']
s3_url = config['hosts']['local']['url']

# obs: verify=False disabling ssl check (Af proxy error)
s3 = boto3.resource('s3',
                    endpoint_url=s3_url,
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1',
                    verify=False)

bucket = s3.Bucket('employer')

print('file saved s3')
print('listing current data in bucket:')

all_keys = []
for obj in bucket.objects.all():
    print(obj.key, obj.size, obj.last_modified)
    all_keys.append(obj.key)
    if download_all == True:
        print('download')
        if 'stream_ads/' in obj.key:
            bucket.download_file(obj.key, obj.key.split('/')[1])



print('end')