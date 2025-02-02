import boto3
import json
import psycopg2

def get_secret(secret_name, region_name="your-region"):
    client = boto3.client('secretsmanager', region_name='sa-east-1')

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    
    return secret

def send_to_postgresql():
    secret_name = "your-secret-name"
    secret = get_secret(secret_name)

    # Połączenie z bazą danych
    conn = psycopg2.connect(
        dbname=secret["dbname"],
        user=secret["user"],
        password=secret["password"],
        host=secret["host"],
        port=secret["port"]
    )

    cursor = conn.cursor()

    # Przykładowa operacja INSERT
    query = "INSERT INTO users (name, email) VALUES (%s, %s);"
    data = ("Jan Kowalski", "jan@example.com")

    cursor.execute(query, data)
    conn.commit()

    cursor.close()
    conn.close()

    print("Dane wysłane do PostgreSQL!")

send_to_postgresql()

