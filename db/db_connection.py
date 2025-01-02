# db/db_connection.py

import psycopg2
from config.config import Config

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = connection.cursor()
        print("Database connection successful.")
        return connection, cursor
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None, None

def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
