# Railway Deployment Guide

This guide will help you deploy the backend to Railway.

## Prerequisites

1. A Railway account (sign up at https://railway.app)
2. GitHub repository with your code
3. All environment variables ready

## Step 1: Connect Railway to GitHub

1. Go to https://railway.app and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the branch (usually `main` or `master`)

## Step 2: Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

## Step 3: Configure Environment Variables

In your Railway project, go to "Variables" and add the following:

### Required Variables:
- `DATABASE_URL` - Automatically set by Railway when you add PostgreSQL
- `ELEVENLABS_API_KEY` - Your ElevenLabs API key
- `EASYPAY_API_KEY` - Your Easypaisa API key
- `EASYPAY_MERCHANT_ID` - Your Easypaisa merchant ID
- `EASYPAY_STORE_ID` - Your Easypaisa store ID
- `JWT_SECRET` - A secure random string for JWT tokens
- `JWT_ALGORITHM` - Set to `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Set to `30`
- `CLAID_API_KEY` - Your Claid API key

### Optional Variables:
- `NETLIFY_URL` - Your Netlify frontend URL (e.g., `https://your-app.netlify.app`)
- `CORS_ALLOW_ALL` - Set to `true` if you want to allow all origins (not recommended for production)
- `PORT` - Railway automatically sets this, but you can override if needed

## Step 4: Configure Service Settings

1. In your Railway service settings:
   - **Root Directory**: Set to `backend` (since your backend code is in the backend folder)
   - **Start Command**: Railway will use the Procfile automatically
   - **Build Command**: Railway will detect Python and install dependencies automatically

2. If Railway doesn't detect the backend folder automatically:
   - Go to Settings → Source
   - Set Root Directory to `backend`

## Step 5: Deploy

1. Railway will automatically deploy when you push to your GitHub repository
2. You can also manually trigger a deployment from the Railway dashboard
3. Check the "Deployments" tab to see the deployment status
4. Once deployed, Railway will provide you with a public URL (e.g., `https://your-app.up.railway.app`)

## Step 6: Update Frontend API URL

1. Update your Netlify environment variables:
   - Add `VITE_API_URL` or `REACT_APP_API_URL` with your Railway backend URL
   - Example: `https://your-app.up.railway.app`

2. Redeploy your Netlify site

## Step 7: Run Database Migrations

Railway will automatically run migrations on startup (configured in the Procfile):
```
alembic upgrade head
```

If you need to run migrations manually:
1. Go to your Railway service
2. Click on "Deployments"
3. Click on the latest deployment
4. Open the terminal/console
5. Run: `alembic upgrade head`

## Troubleshooting

### Database Connection Issues
- Ensure `DATABASE_URL` is set correctly
- Check that PostgreSQL service is running
- Verify the database credentials

### CORS Issues
- Add your Netlify URL to `NETLIFY_URL` environment variable
- Or set `CORS_ALLOW_ALL=true` for testing (not recommended for production)

### Build Failures
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility
- Check Railway build logs for specific errors

### Port Issues
- Railway automatically sets the `PORT` environment variable
- Ensure your application uses `$PORT` or `os.getenv("PORT", "8000")`

## Monitoring

1. **Logs**: View real-time logs in the Railway dashboard
2. **Metrics**: Monitor CPU, memory, and network usage
3. **Deployments**: Track deployment history and rollback if needed

## Custom Domain (Optional)

1. Go to your Railway service settings
2. Click "Generate Domain" or "Custom Domain"
3. Add your custom domain
4. Update DNS records as instructed

## Environment Variables Reference

```env
# Database (Auto-set by Railway)
DATABASE_URL=postgresql://user:password@host:port/database

# API Keys
ELEVENLABS_API_KEY=your_key_here
CLAID_API_KEY=your_key_here
EASYPAY_API_KEY=your_key_here
EASYPAY_MERCHANT_ID=your_merchant_id
EASYPAY_STORE_ID=your_store_id

# JWT
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
NETLIFY_URL=https://your-app.netlify.app
CORS_ALLOW_ALL=false

# Port (Auto-set by Railway)
PORT=8000
```

## Support

If you encounter issues:
1. Check Railway logs for error messages
2. Verify all environment variables are set
3. Ensure database migrations have run successfully
4. Check Railway status page for service outages

