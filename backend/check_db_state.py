"""
Check the current state of the database.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get DATABASE_URL - use SQLite by default if not set
database_url = os.getenv("DATABASE_URL")
if not database_url:
    database_url = "sqlite:///./myaistudio.db"
    print("⚠️ DATABASE_URL not found, using SQLite default: sqlite:///./myaistudio.db")

print("🔍 Checking database state...")

try:
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        # Check if alembic_version table exists
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"📋 Tables in database: {tables}")
        
        if 'alembic_version' in tables:
            print("\n✅ alembic_version table exists")
            # Check its structure
            result = connection.execute(text("""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns 
                WHERE table_name = 'alembic_version'
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            print("📊 alembic_version table structure:")
            for col in columns:
                print(f"   - {col[0]}: {col[1]}" + (f"({col[2]})" if col[2] else ""))
            
            # Check current version
            result = connection.execute(text("SELECT version_num FROM alembic_version;"))
            version = result.fetchone()
            if version:
                print(f"📌 Current Alembic version: {version[0]}")
            else:
                print("📌 No version recorded in alembic_version table")
        else:
            print("\n❌ alembic_version table does not exist")
            print("   This means migrations haven't been run yet, or the table was dropped")
        
except Exception as e:
    print(f"❌ Error checking database: {e}")
    exit(1)




