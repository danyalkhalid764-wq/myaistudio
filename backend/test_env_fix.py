"""
Quick test to verify .env file loads correctly.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

print("📂 Loading .env file...")
try:
    # Load from backend/.env explicitly
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    print(f"   Looking for .env at: {env_path}")
    
    if not os.path.exists(env_path):
        print(f"❌ .env file not found at: {env_path}")
        exit(1)
    
    load_dotenv(env_path, override=True)
    print("✅ .env file loaded successfully")
except Exception as e:
    print(f"❌ Error loading .env file: {e}")
    exit(1)

# Get DATABASE_URL - use SQLite by default if not set
database_url = os.getenv("DATABASE_URL")
if not database_url:
    database_url = "sqlite:///./myaistudio.db"
    print("⚠️ DATABASE_URL not found, using SQLite default: sqlite:///./myaistudio.db")

print(f"✅ DATABASE_URL found: {database_url[:50]}...")

# Test connection
print("\n🔌 Testing database connection...")
try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)

print("\n🎉 All tests passed!")




