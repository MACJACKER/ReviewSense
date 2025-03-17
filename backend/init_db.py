from database import Base, engine
import models
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Print created tables
        print("\nCreated tables:")
        for table in Base.metadata.tables.keys():
            print(f"- {table}")
            
    except Exception as e:
        print("❌ Failed to create database tables!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    init_database() 