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
#print(json.dumps(lt_res, indent=4))

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
ref_res = asg_client.describe_instance_refreshes(
    AutoScalingGroupName=asg_name,
    InstanceRefreshIds=[
        asg_res['InstanceRefreshId'],
    ]
)

ref_status = ref_res['InstanceRefreshes'][0]['Status']
print(ref_status)
print(json.dumps(ref_res['InstanceRefreshes'],indent=4))
time.sleep(1)

ref_status = ref_res['InstanceRefreshes'][0]['Status']
print(ref_status)
print(json.dumps(ref_res['InstanceRefreshes'],indent=4)

#while ref_status == 'Pending' or ref_status == 'InProgress':
#    print(json.dumps(ref_res['InstanceRefreshes'],indent=4))
#    ref_status = ref_res['InstanceRefreshes'][0]['Status']
