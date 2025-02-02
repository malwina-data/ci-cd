import boto3
import json
import psycopg2
from psycopg2 import OperationalError

# Tworzymy klienta do AWS Secrets Manager
client = boto3.client('secretsmanager', region_name='sa-east-1')

# Pobieramy dane logowania z AWS Secrets Manager
response_secret_login = client.get_secret_value(SecretId="db-secret-05")
secret_login = response_secret_login['SecretString']
secret_login_json = json.loads(secret_login)

# Zmienna przechowująca dane logowania
dbname = secret_login_json['dbname']
password = secret_login_json['password']
username = secret_login_json['username']

# Pobieramy ciąg połączenia (connection string) z Secrets Manager
response_string_secret = client.get_secret_value(SecretId="db_connection_secret_03")
secret_string_con = response_string_secret['SecretString']
secret_data_con = json.loads(secret_string_con)

# Zmienna przechowująca connection string (używamy go do połączenia)
connection_string = secret_data_con['connection_string']

# Jeśli potrzebujesz, użyj 'connection_string' do połączenia, lub osobnych danych (dbname, username, password)
# Tworzymy klienta RDS (jeśli chcesz używać IAM DB Authentication)
rds_client = boto3.client('rds', region_name='sa-east-1')

# Generowanie tokenu IAM
hostname = "terraform-20250201120928639400000004.cneu60kskjor.sa-east-1.rds.amazonaws.com"
port = 5432
token = rds_client.generate_db_auth_token(DBHostname=hostname, Port=port, DBUsername=username)

# Łączenie z bazą danych przy użyciu tokenu IAM (tu możesz użyć tokenu z Secrets Managera)
try:
    # Używamy psycopg2 do połączenia z PostgreSQL
    connection = psycopg2.connect(host=hostname,port=port,user=username,password=token,dbname=dbname,sslmode='require')
    print("Połączono z bazą danych!")
except OperationalError as e:
    print(f"Nie udało się połączyć z bazą danych: {e}")
finally:
    if connection:
        connection.close()
