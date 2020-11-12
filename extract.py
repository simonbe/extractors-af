from datetime import date
from datetime import datetime, timedelta
import requests
import json
import boto3
from botocore.client import Config
import os

store_s3 = True
secrets_from_env = False

if secrets_from_env == True:
    config = { 'api_key': os.getenv('API_KEY'),
            'directory': os.getenv('DIRECTORY'),
            'hosts': {'local': {'accessKey': os.getenv('S3_ACCESSKEY'),
            'api': os.getenv('S3_API'), 'lookup': os.getenv('S3_LOOKUP'), 
            'secretKey': os.getenv('S3_SECRETKEY'), 'url': os.getenv('S3_URL')}} }
else:
    with open('config.json', 'r') as f:
        config = json.load(f)

print('config:', config)

api_key = config['api_key']
directory = config['directory']
accessKey = config['hosts']['local']['accessKey']
api = config['hosts']['local']['api']
lookup = config['hosts']['local']['lookup']
secretKey = config['hosts']['local']['secretKey']
s3_url = config['hosts']['local']['url']

yesterday = datetime.strftime(datetime.now() - timedelta(19), '%Y-%m-%d')
today_date = date.today()
from_date = yesterday

print('from_date: ', from_date)

api_url = 'https://jobstream.api.jobtechdev.se/stream'
headers = {'accept': 'application/json', 'api-key': api_key}
date_url = '?date='+str(from_date)
print('api_url', api_url)
print('data_url', date_url)

print('fetching results')

resp = requests.get(api_url+date_url,headers=headers)
result = resp.json()

print('length result:', len(result))
#print(result)

# local save
filename_local = directory + 'stream_ads_date_now_' + str(today_date) + '_from_' + str(from_date) + '.json' 

print('filename local:', filename_local)
with open(filename_local, 'w') as f:
    json.dump(result, f)

print('file saved locally')

# s3 save
if store_s3 == True:

    s3 = boto3.resource('s3',
                    endpoint_url=s3_url,
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

    print('listing current data in bucket:')

    bucket = s3.Bucket('employer')

    s3_filename = 'stream_ads/stream_ads_date_now_' + str(today_date) + '_from_' + str(from_date) + '.json'
    print('filename s3:',s3_filename)
    
    bucket.upload_file(filename_local,s3_filename)
    
    print('file saved s3')
    print('listing current data in bucket:')

    for my_bucket_object in bucket.objects.all():
        print(my_bucket_object)

    print('end s3')

print('end')
