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
lt_id = 'lt-005ab451cba87f311'
src_vers = '27'
asg_name = 'MagentoWEB-ASG1'

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
ami_id = ami_res['Images'][0]['ImageId']
'''
# Create new 'Launch Template' version
lt_res = ec2_client.create_launch_template_version(
    LaunchTemplateData={
        'ImageId': ami_id,
    },
    LaunchTemplateId=lt_id,
    SourceVersion=src_vers,
    VersionDescription='BUILD_NUMBER:' + build_number + ', DATE:' + timestamp,
)
print('New LT version was created:')
print (lt_res['LaunchTemplateVersion']['LaunchTemplateData']['ImageId'])
print (lt_res['LaunchTemplateVersion']['VersionNumber'])
'''

# ASG 'Instance Refresh'
asg_client = boto3.client('autoscaling')
asg_res = asg_client.start_instance_refresh(
    AutoScalingGroupName=asg_name,
    Strategy='Rolling',
    Preferences={
        'MinHealthyPercentage': 0,
        'InstanceWarmup': 0
    }
)

# Describe 'Instance Refresh' status
def refresh_status():
    status = asg_client.describe_instance_refreshes(
        AutoScalingGroupName=asg_name,
        InstanceRefreshIds=[
            asg_res['InstanceRefreshId'],
        ]
    )
    return status

ref_status = 'Pending'
while ref_status == 'Pending' or ref_status == 'InProgress':
    ref_res = refresh_status()
    ref_status = ref_res['InstanceRefreshes'][0]['Status']
    pprint.pprint(ref_res['InstanceRefreshes'])
    print('-')*80
    print('\n')
    time.sleep(10)

if ref_status != 'Successful':
    raise Exception("ASG update failed.\nASG name:" + asg_name + "\nInstance Refresh ID:" + asg_res['InstanceRefreshId'] + "\nStatus:" + ref_status)
