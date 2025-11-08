"""
Initialize Alembic version table with correct column size.
This script creates the alembic_version table with VARCHAR(255) to support longer version names.
This is a safety script that runs before Alembic migrations.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get DATABASE_URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("❌ DATABASE_URL not found in environment variables")
    exit(1)

print("🔧 Ensuring Alembic version table has correct structure...")

try:
    engine = create_engine(database_url)
    
    with engine.begin() as connection:
        # Check if alembic_version table exists
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'alembic_version';
        """))
        exists = result.fetchone() is not None
        
        if exists:
            print("✅ alembic_version table exists")
            # Check and fix column size if needed
            result = connection.execute(text("""
                SELECT character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'alembic_version' 
                AND column_name = 'version_num';
            """))
            current_size = result.fetchone()
            if current_size and current_size[0]:
                if current_size[0] < 255:
                    print(f"🔨 Current column size is {current_size[0]}, expanding to 255...")
                    connection.execute(text("""
                        ALTER TABLE alembic_version 
                        ALTER COLUMN version_num TYPE VARCHAR(255);
                    """))
                    print("✅ Column size updated to VARCHAR(255)")
                else:
                    print(f"✅ Column size is already sufficient ({current_size[0]})")
            else:
                print("⚠️  Could not determine current column size")
        else:
            print("📝 Creating alembic_version table with VARCHAR(255)...")
            # Create the table with the correct column size
            connection.execute(text("""
                CREATE TABLE alembic_version (
                    version_num VARCHAR(255) NOT NULL,
                    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
                );
            """))
            print("✅ alembic_version table created successfully")
        
except Exception as e:
    print(f"⚠️  Warning: Could not ensure alembic_version table structure: {e}")
    print("   Alembic will handle this, but may create table with default size")
    import traceback
    traceback.print_exc()
    # Don't exit - let Alembic handle it

print("✅ Alembic version table check complete.")

