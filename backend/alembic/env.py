from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, DATABASE_URL
from models import User, VoiceHistory, Payment, GeneratedVideo  # ensure all models are imported

# Load .env
load_dotenv()

# Alembic Config object
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata

# Get database URL from .env
def get_url():
    # Use DATABASE_URL from environment or fallback to application's DATABASE_URL
    url = os.getenv("DATABASE_URL") or DATABASE_URL
    if not url:
        # Use SQLite by default if not set
        url = "sqlite:///./myaistudio.db"
    return url

def ensure_alembic_version_table(connection):
    """
    Ensure alembic_version table exists with correct column size.
    Supports both SQLite and PostgreSQL.
    """
    try:
        # Detect database type from connection
        db_type = connection.dialect.name
        
        if db_type == 'sqlite':
            # SQLite: Check if table exists
            result = connection.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='alembic_version';
            """))
            exists = result.fetchone() is not None
            
            if not exists:
                # Create table with TEXT (no size limit in SQLite)
                connection.execute(text("""
                    CREATE TABLE alembic_version (
                        version_num TEXT NOT NULL PRIMARY KEY
                    );
                """))
                print("Created alembic_version table (SQLite)")
        else:
            # PostgreSQL: Check if table exists
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alembic_version';
            """))
            exists = result.fetchone() is not None
            
            if exists:
                # Check current column size
                result = connection.execute(text("""
                    SELECT character_maximum_length 
                    FROM information_schema.columns 
                    WHERE table_name = 'alembic_version' 
                    AND column_name = 'version_num';
                """))
                current_size = result.fetchone()
                if current_size and current_size[0] and current_size[0] < 255:
                    # Alter column to support longer version names
                    connection.execute(text("""
                        ALTER TABLE alembic_version 
                        ALTER COLUMN version_num TYPE VARCHAR(255);
                    """))
                    print(f"Fixed alembic_version.version_num column size from {current_size[0]} to 255")
            else:
                # Create table with correct column size
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS alembic_version (
                        version_num VARCHAR(255) NOT NULL,
                        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
                    );
                """))
                print("Created alembic_version table with VARCHAR(255) (PostgreSQL)")
    except Exception as e:
        print(f"Warning: Could not ensure alembic_version table structure: {e}")
        # Don't fail migrations if this check fails

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        configuration = {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        # Ensure alembic_version table has correct structure before running migrations
        ensure_alembic_version_table(connection)
        connection.commit()
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
