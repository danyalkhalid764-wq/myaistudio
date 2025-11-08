# Railway SQLite Setup Guide

## Setting DATABASE_URL in Railway

To use SQLite on Railway, you need to set the `DATABASE_URL` environment variable in your Railway backend service.

### Steps:

1. **Go to Railway Dashboard**
   - Open your backend service
   - Click on "Variables" tab

2. **Add DATABASE_URL Variable**
   - Click "New Variable"
   - Variable name: `DATABASE_URL`
   - Variable value: `sqlite:///./myaistudio.db`
   - Click "Add"

3. **Save and Redeploy**
   - Railway will automatically redeploy
   - The backend will now use SQLite database

### Important Notes:

- SQLite database file will be created in the backend directory on Railway
- The database file persists between deployments
- SQLite works fine for Railway if you don't need PostgreSQL features
- For production with high traffic, PostgreSQL is recommended, but SQLite works for most use cases

### Verify Setup:

After deployment, check the logs. You should see:
```
Using SQLite database
   Database file: /app/myaistudio.db
```

Instead of:
```
ERROR: DATABASE_URL not found in Railway environment!
```

