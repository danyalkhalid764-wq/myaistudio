# Railway Database Setup Guide

## How to Connect PostgreSQL to Your Backend Service

### Option 1: Automatic Connection (Recommended)

1. **In Railway Dashboard:**
   - Go to your PostgreSQL service
   - Click on the service name
   - Go to the "Variables" tab
   - Find the `DATABASE_URL` variable
   - Click the "..." menu next to it
   - Select "Reference Variable" or "Copy Variable"

2. **In Your Backend Service:**
   - Go to your backend service
   - Click on "Variables" tab
   - Click "New Variable"
   - Variable name: `DATABASE_URL`
   - Variable value: Click "Reference" and select your PostgreSQL service's `DATABASE_URL`
   - Or manually copy the value from PostgreSQL service

### Option 2: Manual Setup

1. **Get PostgreSQL Connection String:**
   - In Railway, go to your PostgreSQL service
   - Click on "Variables" tab
   - Copy the `DATABASE_URL` value (it looks like: `postgresql://user:password@host:port/database`)

2. **Set in Backend Service:**
   - Go to your backend service
   - Click on "Variables" tab
   - Click "New Variable"
   - Variable name: `DATABASE_URL`
   - Variable value: Paste the connection string you copied
   - Save

### Option 3: Use Railway Service Reference

If Railway supports service references, you can use:
- Variable name: `DATABASE_URL`
- Variable value: `${{Postgres.DATABASE_URL}}` (replace "Postgres" with your PostgreSQL service name)

## Verify Setup

After setting DATABASE_URL:
1. Railway will automatically redeploy
2. Check the deployment logs
3. You should see: "Using PostgreSQL database: ..." instead of "Using SQLite database"

## Troubleshooting

If you still see "DATABASE_URL not found":
1. Make sure the variable is set in your **backend service**, not just the PostgreSQL service
2. Check that the variable name is exactly `DATABASE_URL` (case-sensitive)
3. Verify the PostgreSQL service is running
4. Try redeploying the backend service

