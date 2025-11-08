"""
Test script to verify Railway PostgreSQL connection.
This script loads the .env file and tests the database connection.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
print("📂 Loading .env file...")
try:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    print(f"   Looking for .env at: {env_path}")
    
    if not os.path.exists(env_path):
        print(f"❌ .env file not found at: {env_path}")
        exit(1)
    
    # Try loading with override to ensure it loads
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

print(f"\n🔗 DATABASE_URL: {database_url}")
print("   (Password hidden for security)")

# Create SQLAlchemy engine
print("\n🔌 Creating database connection...")
try:
    engine = create_engine(database_url)
    print("✅ Engine created successfully")
except Exception as e:
    print(f"❌ Error creating engine: {e}")
    exit(1)

# Test connection
print("\n🧪 Testing database connection...")
try:
    with engine.connect() as connection:
        # Execute a simple query
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connected to Railway PostgreSQL successfully!")
        print(f"📊 PostgreSQL version: {version}")
        
        # Test if we can query the database
        result = connection.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]
        print(f"📁 Database name: {db_name}")
        
        # Test if tables exist
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result.fetchall()]
        if tables:
            print(f"📋 Found {len(tables)} table(s): {', '.join(tables)}")
        else:
            print("📋 No tables found (database is empty)")
        
except Exception as e:
    print(f"❌ Error connecting to database: {e}")
    exit(1)

print("\n🎉 All tests passed! Database connection is working correctly.")

