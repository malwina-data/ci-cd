import psycopg2
from psycopg2 import sql

def get_connection():
    try:
        # Konfiguracja połączenia
        conn = psycopg2.connect(
            host="terraform-20250202092136305400000004.cneu60kskjor.sa-east-1.rds.amazonaws.com",
            database="db_postgres",
            user="db_admin",
            password="YOUR_PASSWORD_HERE",  # wstaw swoje hasło
            port=5432
        )
        print("Połączono z bazą danych PostgreSQL!")
        return conn
    except Exception as e:
        print(f"Błąd połączenia: {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Wykonaj przykładowe zapytanie, np. sprawdź wersję bazy danych
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print("Wersja PostgreSQL:", db_version)
        except Exception as e:
            print(f"Błąd zapytania: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    test_connection()

