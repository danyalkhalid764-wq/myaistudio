from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration: Use SQLite for local development, PostgreSQL for production
# Check multiple possible Railway variable names for PostgreSQL connection
# Railway typically uses DATABASE_URL, but may use service-specific names
DATABASE_URL = (
    os.getenv("DATABASE_URL") or  # Standard Railway variable (most common)
    os.getenv("POSTGRES_URL") or  # Alternative Railway variable
    os.getenv("PGDATABASE") or    # PostgreSQL standard variable
    os.getenv("POSTGRES_DATABASE_URL") or  # Another possible Railway variable
    os.getenv("POSTGRES_PRIVATE_URL") or  # Railway private URL
    os.getenv("POSTGRES_PUBLIC_URL") or   # Railway public URL
    None
)

if not DATABASE_URL:
    # Use SQLite for both local development and Railway
    # SQLite works fine for Railway if you want a simple database solution
    DATABASE_URL = "sqlite:///./myaistudio.db"
    print("Using SQLite database")
    print(f"   Database file: {os.path.abspath('./myaistudio.db')}")
else:
    # Clean up Railway template variables if present
    if "${{" in DATABASE_URL:
        print("Warning: DATABASE_URL contains template variable, Railway should expand this automatically")
    print(f"Using PostgreSQL database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Required for SQLite
        echo=False  # Set to True for SQL query logging
    )
else:
    # PostgreSQL configuration with lazy connection
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=300,    # Recycle connections after 5 minutes
        connect_args={
            "connect_timeout": 10,  # 10 second timeout
        },
        poolclass=None,  # Use default pool
        # Don't connect on engine creation - connect lazily when needed
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()