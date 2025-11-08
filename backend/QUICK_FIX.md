# Quick Fix for Local Development

## The Problem

1. **Database connection failing** - Railway database might be paused or not accessible
2. **Import error** - Happens because database connection fails during import

## Quick Fix: Start Server Without Database Connection

The server will start, but database operations will fail until database is accessible.

### Commands to Run in PyCharm:

```bash
# Make sure you're in backend folder
cd backend

# Activate venv (if not already)
.\.venv\Scripts\activate

# Start server (will work even if database is not accessible)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## For Production (Railway)

The server on Railway works fine because:
- Railway database is always accessible from Railway services
- DATABASE_URL is automatically set
- Migrations run on startup

## If You Need Database Locally

### Option 1: Use Local PostgreSQL

1. Install PostgreSQL locally
2. Create database: `createdb myaistudio`
3. Update .env: `DATABASE_URL=postgresql://postgres:password@localhost:5432/myaistudio`
4. Run migrations: `alembic upgrade head`

### Option 2: Check Railway Database

1. Go to Railway dashboard
2. Check if PostgreSQL service is running
3. If paused, restart it
4. Test connection: `python test_db_connection.py`


