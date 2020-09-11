import boto3
import time
import pprint
import json
import sys
import os
import re

def update_hosts (tag_value, hosts_name):
    hosts_path = './ansible-jenkins/inventories/hosts'

    # get ip address by tag=Name value=<value>
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
                    tag_value,
                ]
            },
        ]
    )

    ip = ec2_res['Reservations'][0]['Instances'][0]['PublicIpAddress']

    # update hosts file
    f = open(hosts_path,'r')
    str_in = f.read()
    str_out = re.sub(hosts_name + ' ansible_host=\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}', hosts_name + ' ansible_host='+ip,str_in)
    f.close()
    f = open(hosts_path,'w')
    f.write(str_out)
    f.close()

    print('hosts file updated.\n' + hosts_name +':'+ ip)

def clean_ami(num):
    ec2_client = boto3.client('ec2')
    ami_pattern = 'app_*'

    # get AMI List by pattern
    ami_list = ec2_client.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values': [
                ami_pattern,
            ]
        },
    ]
    )
    pprint.pprint(ami_list)
    # get AMI IDs which should be deleted
    def ami_sort(e):
        res = re.search('_(\d+)_', e['Name'])
        return int(res[1])

    ami_list.sort(key=ami_sort)

    if len(ami_list) > num:
        ami_del = ami_list[:(len(ami_list) - num)]
        for i in ami_del['ImageId']:
            print(i)

# run func
if sys.argv[1] == 'update_hosts':
    update_hosts('MagentoAdmin', 'admin')

if sys.argv[1] == 'clean_ami':
    clean_ami(1)
