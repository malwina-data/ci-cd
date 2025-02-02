import boto3

def list_secrets(region="sa-east-1"):
    client = boto3.client('secretsmanager', region_name=region)
    response = client.list_secrets()
    for secret in response.get('SecretList', []):
        print(f"Name: {secret.get('Name')}, ARN: {secret.get('ARN')}")

if __name__ == "__main__":
    list_secrets()
