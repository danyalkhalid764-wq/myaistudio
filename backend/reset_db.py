from sqlalchemy import text
from database import Base, engine
from models import User, VoiceHistory, Payment

print("Dropping old tables (cascade)...")

with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE;"))
    conn.execute(text("CREATE SCHEMA public;"))
    conn.commit()

print("Creating new tables...")
Base.metadata.create_all(bind=engine)

print("✅ Database reset successfully!")
