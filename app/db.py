import psycopg2
import os

# Establish a connection to the PostgreSQL server
def connect_to_database():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        with conn.cursor() as cur:
            cur.execute('SET search_path TO public')
            conn.commit()
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
        return None   


