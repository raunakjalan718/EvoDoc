import os
import subprocess
from pathlib import Path
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
from src.db.config import engine, Base

def create_postgres_db():
    """Create PostgreSQL database if it doesn't exist"""
    load_dotenv()
    
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "evodoc")
    
    if not database_exists(engine.url):
        print(f"Creating database {DB_NAME}...")
        create_database(engine.url)
        print(f"Database {DB_NAME} created.")
    else:
        print(f"Database {DB_NAME} already exists.")

def create_tables():
    """Create database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    # Create database if using PostgreSQL
    if "postgresql" in str(engine.url):
        create_postgres_db()
    
    # Create tables
    create_tables()
    
    print("Database setup complete!")
