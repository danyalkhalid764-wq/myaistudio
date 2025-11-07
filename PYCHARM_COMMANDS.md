# PyCharm Commands - Manual Setup

## Step 1: Navigate to Backend Directory

```bash
cd backend
```

## Step 2: Activate Virtual Environment (if using one)

**If you have a virtual environment:**
```bash
# Windows
.\venv\Scripts\activate

# Or if using .venv
.\.venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Set Environment Variables

**Create or update .env file in backend folder:**

```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://postgres:ZwsAwpZpQqRowzhxbySTaVJVwwNMrWGj@nozomi.proxy.rlwy.net:39764/railway"
$env:ELEVENLABS_API_KEY="your_elevenlabs_key_here"
$env:EASYPAY_API_KEY="your_easypay_key_here"
$env:EASYPAY_MERCHANT_ID="your_merchant_id_here"
$env:EASYPAY_STORE_ID="your_store_id_here"
$env:CLAID_API_KEY="your_claid_key_here"
$env:JWT_SECRET="your_jwt_secret_here"
$env:JWT_ALGORITHM="HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

**Or create .env file manually:**
```bash
# Create .env file with this content:
DATABASE_URL=postgresql://postgres:ZwsAwpZpQqRowzhxbySTaVJVwwNMrWGj@nozomi.proxy.rlwy.net:39764/railway
ELEVENLABS_API_KEY=your_elevenlabs_key_here
EASYPAY_API_KEY=your_easypay_key_here
EASYPAY_MERCHANT_ID=your_merchant_id_here
EASYPAY_STORE_ID=your_store_id_here
CLAID_API_KEY=your_claid_key_here
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Step 5: Test Database Connection

```bash
python test_db_connection.py
```

**Expected output:**
```
✅ Connected to Railway PostgreSQL successfully!
```

## Step 6: Initialize Alembic Version Table

```bash
python init_alembic_version.py
```

**Expected output:**
```
✅ Created alembic_version table with VARCHAR(255)
```

## Step 7: Run Database Migrations

```bash
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial migration
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002_add_generated_images
...
```

## Step 8: Check Database State

```bash
python check_db_state.py
```

**Expected output:**
```
📋 Tables in database: ['alembic_version', 'users', 'voice_history', ...]
✅ alembic_version table exists
📊 alembic_version table structure:
   - version_num: character varying(255)
```

## Step 9: Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 10: Test the API

**Open in browser or use curl:**

```bash
# Health check
curl http://localhost:8000/health

# API docs
# Open in browser: http://localhost:8000/docs
```

## Quick Setup Script (All in One)

```bash
# Navigate to backend
cd backend

# Activate venv (if using)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test database connection
python test_db_connection.py

# Initialize Alembic version table
python init_alembic_version.py

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting Commands

**If database connection fails:**
```bash
python test_db_connection.py
```

**If migrations fail:**
```bash
# Check current migration state
alembic current

# Check migration history
alembic history

# Fix version table manually
python init_alembic_version.py
```

**If server won't start:**
```bash
# Check if port is in use
netstat -ano | findstr :8000

# Or use different port
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## Environment Variables in PyCharm

**To set environment variables in PyCharm:**

1. Go to Run → Edit Configurations
2. Click "+" → Python
3. Set:
   - Script path: `backend/main.py`
   - Working directory: `backend`
   - Environment variables: Add all your env vars here
4. Or use .env file (recommended)

