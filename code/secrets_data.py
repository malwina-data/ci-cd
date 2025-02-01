import boto3
import json
import base64


client = boto3.client('secretsmanager', region_name='sa-east-1')
response_secret_login = client.get_secret_value(SecretId="db-secret-05")
secret_login = response_secret_login['SecretString']
secret_login_json = json.loads(secret_login)
dbname = secret_login_json['dbname']
password = secret_login_json['password']
username = secret_login_json['username']

response_string_secret = client.get_secret_value(SecretId="db_connection_secret_03")
secret_string_con = response_string_secret['SecretString']
secret_data_con = json.loads(secret_string_con)
connection_string = secret_data_con['connection_string']

