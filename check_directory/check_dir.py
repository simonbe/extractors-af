from datetime import date
from datetime import datetime, timedelta
import requests
import json
import boto3
from botocore.client import Config
import os

store_s3 = False
secrets_from_env = True

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


print('listing directory' + directory)

from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

print('length files=',len(onlyfiles))

for f in onlyfiles:
    print(f)

print('end')