# Fix Local Development Setup

## Issues Fixed

1. **Import Error:** `config.py` is correct - the issue was database connection failing before import could complete
2. **Database Connection:** Railway database connection is failing - this is expected if the database is not accessible

## Solutions

### Option 1: Use Local Database for Development

1. **Install PostgreSQL locally** or use Docker:
   ```bash
   # Using Docker
   docker run --name postgres-dev -e POSTGRES_PASSWORD=password -e POSTGRES_DB=myaistudio -p 5432:5432 -d postgres
   ```

2. **Update .env file:**
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/myaistudio
   ```

3. **Run migrations:**
   ```bash
   python init_alembic_version.py
   alembic upgrade head
   ```

4. **Start server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Use Railway Database (If Accessible)

1. **Check Railway database is running:**
   - Go to Railway dashboard
   - Check PostgreSQL service is active

2. **Verify DATABASE_URL in .env:**
   ```
   DATABASE_URL=postgresql://postgres:ZwsAwpZpQqRowzhxbySTaVJVwwNMrWGj@nozomi.proxy.rlwy.net:39764/railway
   ```

3. **Test connection:**
   ```bash
   python test_db_connection.py
   ```

4. **If connection fails:**
   - Railway database might be paused (free tier)
   - Check Railway dashboard
   - Restart PostgreSQL service if needed

### Option 3: Skip Database for Testing

If you just want to test the server without database:

1. **Comment out database operations in main.py:**
   - Already done - `Base.metadata.create_all(bind=engine)` is commented out

2. **Start server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Note:** Some endpoints will fail without database, but server will start

## Quick Fix Commands

```bash
# Test database connection
python test_db_connection.py

# If connection works, run migrations
python init_alembic_version.py
alembic upgrade head

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## For Production (Railway)

The server on Railway should work fine because:
- Railway automatically sets DATABASE_URL
- Database is always accessible from Railway services
- Migrations run automatically on startup


