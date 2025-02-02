import boto3

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='sa-east-1')
    response = client.list_secrets()
    secrets_list = []
    for secret in response.get('SecretList', []):
        secrets_list.append(secret.get('Name'))

    # secrets with login and password
    response = client.get_secret_value(SecretId=secrets_list[0])
    secret = response['SecretString']
    secret_dict = json.loads(secret)
    db_username = secret_dict.get('db_username')
    db_password = secret_dict.get('db_password')

    # secrets with endpoint 
    response = client.get_secret_value(SecretId=secrets_list[1])
    secret = response['SecretString']
    secret_dict = json.loads(secret)
    endpoint = secret_dict.get('connection_string')

    print(f"db_username {db_username}")
    print(f"db_password {db_password}")
    print(f"db_username {endpoint}")
    
if __name__ == "__main__":
    get_db_credentials()