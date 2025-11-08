# Fix Railway DATABASE_URL Error

## Problem
Railway is showing repeated errors:
```
❌ DATABASE_URL not found in environment variables
```

## Solution

### Step 1: Set DATABASE_URL in Railway

1. Go to Railway Dashboard: https://railway.app
2. Open your **backend service**
3. Click on **"Variables"** tab
4. Click **"New Variable"**
5. Set:
   - **Variable name**: `DATABASE_URL`
   - **Variable value**: `sqlite:///./myaistudio.db`
6. Click **"Add"**

### Step 2: Verify Setup

After setting the variable, Railway will automatically redeploy. Check the logs - you should see:
```
Using SQLite database
   Database file: /app/myaistudio.db
```

Instead of:
```
❌ DATABASE_URL not found in environment variables
```

### Step 3: If Error Persists

If you still see the error after setting `DATABASE_URL`:

1. **Check Railway Variables Tab**
   - Make sure `DATABASE_URL` is set correctly
   - Make sure there are no typos
   - Make sure the variable is for the **backend service**, not the PostgreSQL service

2. **Check Railway Logs**
   - Look for which script is printing the error
   - The error should stop after setting `DATABASE_URL`

3. **Redeploy**
   - Go to your backend service
   - Click "Deployments"
   - Click "Redeploy" to force a fresh deployment

## Important Notes

- The code is now configured to use SQLite by default if `DATABASE_URL` is not set
- SQLite works fine for Railway deployments
- The database file will persist between deployments
- For high-traffic production, PostgreSQL is recommended, but SQLite works for most use cases

