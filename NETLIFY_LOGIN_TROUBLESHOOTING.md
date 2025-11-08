# Netlify Login/Register Stuck on Processing - Troubleshooting Guide

## 🔍 Most Common Issues

### 1. **VITE_API_URL Not Set in Netlify** ⚠️ (MOST LIKELY ISSUE)

**Problem**: The frontend is trying to connect to `http://localhost:8000` instead of your Railway backend.

**Solution**:
1. Go to your Netlify site dashboard
2. Navigate to **Site settings** → **Environment variables**
3. Add a new variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-railway-backend.railway.app` (replace with your actual Railway URL)
4. **Redeploy** your site (or trigger a new build)

**How to check**: Open browser console (F12) and look for:
```
🔗 API Base URL: http://localhost:8000  ❌ (Wrong - should be your Railway URL)
🔗 VITE_API_URL env var: undefined  ❌ (Not set)
```

### 2. **CORS Not Configured**

**Problem**: Backend is blocking requests from Netlify domain.

**Solution**: Make sure your Railway backend has CORS configured. Check `backend/main.py`:
- Should include: `https://picvoice3labc.netlify.app`
- Or your actual Netlify domain

**How to check**: Browser console will show:
```
Network Error - Check if backend is running and CORS is configured
```

### 3. **Backend Not Running**

**Problem**: Railway backend is down or not deployed.

**Solution**: 
1. Check Railway dashboard - is the service running?
2. Test backend directly: `https://your-railway-backend.railway.app/health`
3. Should return: `{"status": "healthy"}`

### 4. **Wrong Backend URL**

**Problem**: The Railway URL in `VITE_API_URL` is incorrect.

**Solution**:
1. Get the correct Railway URL from Railway dashboard
2. Make sure it starts with `https://`
3. Update `VITE_API_URL` in Netlify
4. Redeploy

## 🔧 Quick Fix Steps

1. **Check Browser Console** (F12):
   - Look for error messages
   - Check what API URL is being used
   - Look for CORS errors

2. **Verify Environment Variable**:
   - In Netlify: Site settings → Environment variables
   - Make sure `VITE_API_URL` is set correctly
   - Value should be: `https://your-railway-backend.railway.app`

3. **Test Backend Directly**:
   - Open: `https://your-railway-backend.railway.app/health`
   - Should return: `{"status": "healthy"}`

4. **Redeploy Frontend**:
   - After setting `VITE_API_URL`, trigger a new deployment
   - Or push a new commit to trigger auto-deploy

## 📋 Checklist

- [ ] `VITE_API_URL` is set in Netlify environment variables
- [ ] `VITE_API_URL` points to your Railway backend (starts with `https://`)
- [ ] Railway backend is running and accessible
- [ ] CORS is configured in backend to allow your Netlify domain
- [ ] Frontend has been redeployed after setting environment variable

## 🐛 Debug Information

After deploying the updated build, check browser console for:
- `🔗 API Base URL:` - Should show your Railway URL
- `🔗 VITE_API_URL env var:` - Should show your Railway URL (not undefined)
- Any error messages about network errors or CORS

## ✅ Expected Behavior

When working correctly:
1. User clicks Login/Register
2. Button shows "Signing in..." or "Creating account..."
3. Request is sent to Railway backend
4. Response received (success or error)
5. Button returns to normal state
6. User is redirected or shown error message

If stuck on "processing", the request is likely failing silently.

