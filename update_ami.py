import boto3
import time
import pprint
import json
import sys
import os
'''
how to start:
1) python3 update_ami.py build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id  ## with 'ami_id'
2) python3 update_ami.py build_number, timestamp, branch, lt_id, src_vers, asg_name          ## without 'ami_id'

example:
python3 update_ami.py 13 2020/09/07/02-09-950 master lt-005ab451cba87f311 27 MagentoWEB-ASG1

vars:
build_number - Jenkins build number
branch - Jenkins Git branch/tag
lt_id - Launch Template ID
src_vers - Launch Template Source version
asg_name - AutoScalingGroupName
ami_id - EC2 AMI ID
'''

# Vars
build_number = sys.argv[1]
timestamp = sys.argv[2]
branch = sys.argv[3]
lt_id = sys.argv[4]
src_vers = sys.argv[5]
asg_name = sys.argv[6]
print(sys.argv)
ami_id = sys.argv[7] if len(sys.argv) == 8 else None

def update_ami(build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id):
    ec2_client = boto3.client('ec2')

    # Get AMI ID
    if ami_id is None:
        # AMI Name
        ami_name = 'app_' + build_number + '_' + branch + '_' + timestamp
        print('AMI Name:' + ami_name)

        # AMI ID
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

    print('AMI ID:' + ami_id)

    # Create new 'Launch Template' version
    lt_res = ec2_client.create_launch_template_version(
        LaunchTemplateData={
            'ImageId': ami_id,
        },
        LaunchTemplateId=lt_id,
        SourceVersion=src_vers,
        VersionDescription='BUILD_NUMBER:' + build_number + ', DATE:' + timestamp,
    )
    print('New LT was created.')
    print ('LT Version: ' + str(lt_res['LaunchTemplateVersion']['VersionNumber']))


    # Start ASG 'Instance Refresh'
    asg_client = boto3.client('autoscaling')
    asg_res = asg_client.start_instance_refresh(
        AutoScalingGroupName=asg_name,
        Strategy='Rolling',
        Preferences={
            'MinHealthyPercentage': 0,
            'InstanceWarmup': 0
        }
    )
    print('ASG Instance Refresh started...\n' + 'InstanceRefreshId: ' + asg_res['InstanceRefreshId'])

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
        time.sleep(10)
        ref_res = refresh_status()
        ref_status = ref_res['InstanceRefreshes'][0]['Status']
        pprint.pprint(ref_res['InstanceRefreshes'])
        print('-'*80 + '\n')


    if ref_status != 'Successful':
        raise Exception("ASG update failed.\nASG name:" + asg_name + "\nInstance Refresh ID:" + asg_res['InstanceRefreshId'] + "\nStatus:" + ref_status)

# Run 'update_ami' func
update_ami(build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id)
