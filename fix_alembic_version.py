"""
Fix Alembic version table to allow longer version names.
This script alters the alembic_version table to support version names longer than 32 characters.
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

print("🔧 Fixing Alembic version table...")
print(f"🔗 Connecting to database...")

try:
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        # Check current column size
        result = connection.execute(text("""
            SELECT character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'alembic_version' 
            AND column_name = 'version_num';
        """))
        current_size = result.fetchone()
        if current_size:
            print(f"📊 Current version_num column size: {current_size[0]}")
        
        # Alter the column to allow longer version names (up to 255 characters)
        print("🔨 Altering alembic_version.version_num column to VARCHAR(255)...")
        connection.execute(text("""
            ALTER TABLE alembic_version 
            ALTER COLUMN version_num TYPE VARCHAR(255);
        """))
        connection.commit()
        print("✅ Alembic version table fixed successfully!")
        
        # Verify the change
        result = connection.execute(text("""
            SELECT character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'alembic_version' 
            AND column_name = 'version_num';
        """))
        new_size = result.fetchone()
        if new_size:
            print(f"📊 New version_num column size: {new_size[0]}")
        
except Exception as e:
    print(f"❌ Error fixing Alembic version table: {e}")
    exit(1)

print("\n🎉 Fix complete! You can now run migrations again.")

