import boto3
import json
import psycopg2
from datetime import datetime

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='sa-east-1')
    response = client.list_secrets()
    secrets_list = []
    for secret in response.get('SecretList', []):
        secrets_list.append(secret.get('Name'))

    # secrets with endpoint 
    response = client.get_secret_value(SecretId=secrets_list[0])
    secret = response['SecretString']
    secret_dict = json.loads(secret)
    endpoint = secret_dict.get('connection_string')


    try:
        conn = psycopg2.connect(endpoint)
        print("Połączono z bazą danych")
        cursor = conn.cursor()

        # Wstawianie danych
        with open("./log_1.txt", 'r') as file:
            content = file.read()
        created_at = datetime.now()
        cursor.execute(
        "INSERT INTO data_raw (content, created_at) VALUES (%s, %s)",
        (content, created_at))

        with open("./log_2.txt", 'r') as file:
            content = file.read()
        created_at = datetime.now()
        cursor.execute(
        "INSERT INTO data_raw (content, created_at) VALUES (%s, %s)",
        (content, created_at))

        with open("./log_3.txt", 'r') as file:
            content = file.read()
        created_at = datetime.now()
        cursor.execute(
        "INSERT INTO data_raw (content, created_at) VALUES (%s, %s)",
        (content, created_at))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Nie udało się połączyć z bazą danych: {e}")
if __name__ == "__main__":
    get_db_credentials()