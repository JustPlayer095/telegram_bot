import psycopg2
from psycopg2 import Error
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_database():
    try:
        # Connect to default PostgreSQL database
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"Database {DB_NAME} created successfully")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error creating database: {e}")

def get_db_connection():
    try:
        # First try to create database if it doesn't exist
        create_database()
        
        # Now connect to our database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            client_encoding='utf8'
        )
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def init_db():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    message_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            connection.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

def save_message(user_id, message_text):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO messages (user_id, message_text) VALUES (%s, %s)",
                (user_id, message_text)
            )
            connection.commit()
            return True
        except Error as e:
            print(f"Error saving message: {e}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

def get_user_messages(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT message_text, created_at FROM messages WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            messages = cursor.fetchall()
            return messages
        except Error as e:
            print(f"Error retrieving messages: {e}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

def delete_user_messages(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM messages WHERE user_id = %s",
                (user_id,)
            )
            connection.commit()
            return True
        except Error as e:
            print(f"Error deleting messages: {e}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close()

def get_user_messages_with_ids(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, message_text, created_at FROM messages WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            messages = cursor.fetchall()
            return messages
        except Error as e:
            print(f"Error retrieving messages: {e}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

def delete_specific_message(message_id, user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM messages WHERE id = %s AND user_id = %s",
                (message_id, user_id)
            )
            connection.commit()
            return cursor.rowcount > 0  # Returns True if a message was deleted
        except Error as e:
            print(f"Error deleting message: {e}")
            return False
        finally:
            if connection:
                cursor.close()
                connection.close() 