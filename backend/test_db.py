import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Macjacker@123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "sentiment_db")

print(f"Connecting to database: {DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # Connect to the default PostgreSQL database first
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("Connected to default database!")
    
    # Check if our database exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Creating database {DB_NAME}...")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database {DB_NAME} created!")
    else:
        print(f"Database {DB_NAME} already exists!")
    
    # Close connection to default database
    cursor.close()
    conn.close()
    
    # Connect to our database
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    cursor = conn.cursor()
    print(f"Connected to {DB_NAME} database!")
    
    # Test query
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"Test query result: {result}")
    
    cursor.close()
    conn.close()
    print("Database connection test successful!")
    
except Exception as e:
    print(f"Database connection error: {str(e)}") 