import os
from database import engine, SessionLocal
from models import Base
from sentiment_model import SentimentAnalyzer
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    """Test the database connection"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        print("✅ Database connection successful!")
        db.close()
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {str(e)}")
        return False
    return True

def test_model_loading():
    """Test loading the sentiment analysis model"""
    try:
        analyzer = SentimentAnalyzer.get_instance()
        test_text = "This is a test sentence."
        sentiment, confidence = analyzer.analyze(test_text)
        print("✅ Model loaded successfully!")
        print(f"Test prediction: {sentiment} (confidence: {confidence:.2f})")
    except Exception as e:
        print("❌ Model loading failed!")
        print(f"Error: {str(e)}")
        return False
    return True

def create_database():
    """Create the database if it doesn't exist"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return False

    try:
        # Extract database name from URL
        db_name = db_url.split("/")[-1]
        # Create connection URL without database name
        base_url = "/".join(db_url.split("/")[:-1])
        
        # Connect to PostgreSQL server
        conn = psycopg2.connect(base_url + "/postgres")
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created successfully!")
        else:
            print(f"ℹ️ Database '{db_name}' already exists.")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("❌ Database creation failed!")
        print(f"Error: {str(e)}")
        return False

def create_tables():
    """Create database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print("❌ Database tables creation failed!")
        print(f"Error: {str(e)}")
        return False

def main():
    print("\n🔍 Testing Application Setup\n")
    
    print("1. Creating database...")
    if not create_database():
        return
    
    print("\n2. Creating tables...")
    if not create_tables():
        return
    
    print("\n3. Testing database connection...")
    if not test_database_connection():
        return
    
    print("\n4. Testing model loading...")
    if not test_model_loading():
        return
    
    print("\n✨ All tests completed successfully!")
    print("\nYou can now start the application:")
    print("1. Start the backend: uvicorn main:app --reload")
    print("2. Start the frontend: npm run dev")

if __name__ == "__main__":
    main() 