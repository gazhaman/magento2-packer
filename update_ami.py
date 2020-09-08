import boto3
import time
import pprint
import json
import sys
import os

build_number = '13'
timestamp = '2020/09/07/02-09-950'
branch = 'master'

ami_name = 'app_' + build_number + '-' + branch + '_' + timestamp
print(ami_name)
