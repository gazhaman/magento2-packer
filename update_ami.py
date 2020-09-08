import boto3
import time
import pprint
import json
import sys
import os

# Vars
build_number = '13'
timestamp = '2020/09/07/02-09-950'
branch = 'master'

# AMI Name
ami_name = 'app_' + build_number + '-' + branch + '_' + timestamp

# AMI ID
ec2_client = boto3.client('ec2')
ami_id = client.describe_images(
    Filters=[
        {
            'Name': 'Name',
            'Values': [
                ami_name,
            ]
        }
    ]
)

print(ami_id)
