# SQLite Quick Start - Commands to Run

## ✅ What's Done

1. ✅ Database switched to SQLite for local development
2. ✅ PostgreSQL still works for production (Railway)
3. ✅ All scripts updated to support both databases

## 🚀 Commands to Run in PyCharm Terminal

### Step 1: Remove or Comment DATABASE_URL in .env

**Option A: Delete .env file** (if it only has DATABASE_URL)
```bash
cd backend
Remove-Item .env
```

**Option B: Comment out DATABASE_URL in .env**
```bash
# Edit .env file and comment out:
# DATABASE_URL=postgresql://...
```

### Step 2: Initialize Alembic Version Table

```bash
python init_alembic_version.py
```

**Expected output:**
```
📦 Using SQLite database for local development
🔧 Ensuring Alembic version table has correct structure...
✅ Created alembic_version table (SQLite)
```

### Step 3: Run Migrations

```bash
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial migration
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002_add_generated_images
...
```

### Step 4: Start Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
📦 Using SQLite database for local development
   Database file: D:\pakistaniproject\backend\myaistudio.db
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 📁 Database File Location

SQLite database will be created at:
- `backend/myaistudio.db`

## 🔄 Quick Commands (Copy-Paste All)

```bash
cd backend
python init_alembic_version.py
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Benefits

1. ✅ No database server needed
2. ✅ Works offline
3. ✅ Fast and lightweight
4. ✅ Database file in your project folder
5. ✅ Easy to reset/backup

## 🗑️ Reset Database (If Needed)

```bash
# Delete SQLite database
Remove-Item myaistudio.db

# Re-run migrations
python init_alembic_version.py
alembic upgrade head
```


