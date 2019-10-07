#!/usr/bin/env python
import boto3
import sys
import os
import zipfile


bucket_name = 'jenkins-lambda-upoad'
function_name = 'gog-hello-world'
aws_access_key = os.getenv('AwsAccessKeyDev')
aws_secret_access_key = os.getenv('AwsSecretKeyDev')

# Step 1: Upload from local to S3

f = open('lambda_function.py', 'r')
zip_file = zipfile.ZipFile('lambda.zip', 'w')
zipfile.ZipInfo('lambda_function.py').external_attr = 0777 << 16L
zip_file.write('lambda_function.py', compress_type=zipfile.ZIP_DEFLATED)
zip_file.close()

s3_client = boto3.client('s3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name='eu-west-1',
)

s3_client.upload_file('lambda.zip', bucket_name, 'lambda.zip')

# Step 2: Deploy Lambda from S3

lambda_client = boto3.client('lambda',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name='eu-west-1',
)

response = lambda_client.update_function_code(
    FunctionName=function_name,
    S3Bucket=bucket_name,
    S3Key='lambda.zip',
    Publish=True
)

# Step 3: Invoke Lambda

response = lambda_client.invoke(FunctionName=function_name)

print(response)
print(response['Payload'].read())