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

    ip_admin = ec2_res['Reservations'][0]['Instances'][0]['PublicIpAddress']

    # update hosts file
    f = open(hosts_path,'r')
    str_in = f.read()
    str_out = re.sub(hosts_name + ' ansible_host=\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}', hosts_name + ' ansible_host='+ip_admin,str_in)
    f.close()
    f = open(hosts_path,'w')
    f.write(str_out)
    f.close()

    print('hosts file updated.\n' + hosts_name +':'+ ip_admin)

# run
update_hosts('MagentoAdmin', 'admin')
