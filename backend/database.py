import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Macjacker@123")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "sentiment_db")

# URL encode the password to handle special characters
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Connecting to database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"Using connection string: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection error: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
