# SQLite Setup for Local Development

## ✅ What Changed

1. **Database switched to SQLite** for local development
2. **PostgreSQL still supported** for production (Railway)
3. **Automatic detection** - uses SQLite if DATABASE_URL is not set

## 🚀 Quick Start

### Step 1: Remove DATABASE_URL from .env (for local development)

**Option A: Delete .env file** (if you only have DATABASE_URL in it)
```bash
# In backend folder
Remove-Item .env
```

**Option B: Comment out DATABASE_URL in .env**
```
# DATABASE_URL=postgresql://...
# Commented out to use SQLite for local development
```

### Step 2: Run Migrations

```bash
# Initialize Alembic version table
python init_alembic_version.py

# Run migrations
alembic upgrade head
```

### Step 3: Start Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Database File Location

SQLite database will be created at:
- `backend/myaistudio.db`

This file will contain all your local data.

## 🔄 Switching Between SQLite and PostgreSQL

### For Local Development (SQLite):
- Don't set `DATABASE_URL` in .env
- Or set it to: `sqlite:///./myaistudio.db`

### For Production (PostgreSQL on Railway):
- Railway automatically sets `DATABASE_URL`
- No changes needed - it will use PostgreSQL automatically

## 🗑️ Reset Local Database

If you want to start fresh:

```bash
# Delete SQLite database
Remove-Item myaistudio.db

# Re-run migrations
python init_alembic_version.py
alembic upgrade head
```

## ✅ Benefits of SQLite for Local Development

1. ✅ No database server needed
2. ✅ Fast and lightweight
3. ✅ Database file is in your project folder
4. ✅ Easy to reset/backup
5. ✅ Works offline

## 📝 Commands Summary

```bash
# Navigate to backend
cd backend

# Activate venv
.\.venv\Scripts\activate

# Remove DATABASE_URL from .env (or comment it out)

# Initialize and run migrations
python init_alembic_version.py
alembic upgrade head

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


