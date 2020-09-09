import boto3
import time
import pprint
import json
import sys
import os

ec2_client = boto3.client('ec2')
ec2_res = ec2_client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
        {
            'Name': 'tag:Name',
            'Values': [
                'MagentoAdmin',
            ]
        },
    ]
)

pprint.pprint(ec2_res['Reservations'][0]['Instances'][0]['PublicIpAddress'])
