import boto3
import json
import psycopg2

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='sa-east-1')
    response = client.list_secrets()
    secrets_list = []
    for secret in response.get('SecretList', []):
        secrets_list.append(secret.get('Name'))

    # secrets with endpoint 
    response = client.get_secret_value(SecretId=secrets_list[1])
    secret = response['SecretString']
    secret_dict = json.loads(secret)
    #endpoint = secret_dict.get('connection_string')
    endpoint= "postgresql://db_admin:admin_password@terraform-20250202092136305400000004.cneu60kskjor.sa-east-1.rds.amazonaws.com:5432/db_postgres"


    try:
        conn = psycopg2.connect(endpoint)
        print("Połączono z bazą danych")
        cursor = conn.cursor()
    
        cursor.execute("""
        CREATE TABLE data_raw (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """)
        cursor.execute("""
        CREATE TABLE data_proceed (
        id SERIAL PRIMARY KEY,
        raw_id INTEGER REFERENCES data_raw(id),
        processed_content TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); 
        """)
        conn.commit()

        cursor.execute("SELECT * FROM data_raw")

        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Nie udało się połączyć z bazą danych: {e}")
if __name__ == "__main__":
    get_db_credentials()