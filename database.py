from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL configuration from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Temporary fallback to get the app running
if not DATABASE_URL:
    # Use SQLite as fallback for now
    DATABASE_URL = "sqlite:///./test.db"
    print("⚠️  DATABASE_URL not found, using SQLite fallback")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()