import boto3
import time
import pprint.pprint
import json
import sys
import os

# Vars
build_number = '13'
timestamp = '2020/09/07/02-09-950'
branch = 'master'

# AMI Name
ami_name = 'app_' + build_number + '_' + branch + '_' + timestamp

# AMI ID
ec2_client = boto3.client('ec2')
ami_res = ec2_client.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values': [
                ami_name
            ]
        }
    ]
)

#ami_id = ami_res[]
pprint(ami_id)
