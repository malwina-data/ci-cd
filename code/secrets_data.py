import boto3
import json
from botocore.exceptions import ClientError
import base64

parsed_dict={}
tfvars_file_path = './terraform/terraform.tfvars'
with open(tfvars_file_path, 'r') as file:
    tfvars_content = file.read()
    for line in tfvars_content.strip().splitlines():
        key, value = line.split("=", 1)
        parsed_dict[key.strip()] = value.strip().strip('"')

client = boto3.client('secretsmanager', region_name='sa-east-1')
response_string_secret = client.get_secret_value(SecretId=parsed_dict['secret_2'])
secret_string_con = response_string_secret['SecretString']
secret_data_con = json.loads(secret_string_con)
connection_string = secret_data_con['connection_string']

