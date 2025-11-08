# Netlify Deployment Guide - Complete Setup

## ✅ What's Already Done

1. ✅ Frontend API files use environment variables (`VITE_API_URL`)
2. ✅ Frontend built with Railway URL: `https://pakistani-project-backend.up.railway.app`
3. ✅ `dist` folder is ready for drag-and-drop deployment
4. ✅ `_redirects` file included for SPA routing
5. ✅ Backend CORS configured to accept frontend URLs

## 📦 Your Build is Ready

**Location:** `frontend/dist/`

**Contents:**
- `index.html` - Main HTML file
- `assets/` - CSS and JavaScript bundles (already built with Railway URL)
- `_redirects` - SPA routing configuration

## 🚀 Step 1: Deploy to Netlify (Drag & Drop)

### Option A: Drag and Drop (Quickest)

1. **Go to Netlify:**
   - https://app.netlify.com
   - Sign in

2. **Drag and Drop:**
   - Go to "Sites" tab
   - Drag the `frontend/dist` folder to the Netlify dashboard
   - Netlify will automatically deploy

3. **Get your Netlify URL:**
   - Netlify will provide a URL like: `https://your-app-name.netlify.app`
   - Copy this URL

### Option B: Connect to GitHub (Recommended for Updates)

1. **In Netlify Dashboard:**
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select your repository: `danyalkhalid764-wq/myaistudio`
   - Set build settings:
     - **Base directory:** `frontend`
     - **Build command:** `npm run build`
     - **Publish directory:** `frontend/dist`
     - **Environment variables:**
       - `VITE_API_URL` = `https://pakistani-project-backend.up.railway.app`

2. **Deploy:**
   - Click "Deploy site"
   - Netlify will build and deploy

## 🔧 Step 2: Configure Railway Backend CORS

After you get your Netlify URL, update Railway:

1. **Go to Railway Dashboard:**
   - https://railway.app
   - Click on your backend service: `pakistani-project-backend`

2. **Go to Variables tab:**
   - Add/Update these environment variables:
     - `FRONTEND_URL` = `https://your-netlify-app.netlify.app`
     - `BACKEND_URL` = `https://pakistani-project-backend.up.railway.app`
     - `NETLIFY_URL` = `https://your-netlify-app.netlify.app` (optional, for CORS)

3. **Redeploy Railway:**
   - Go to "Deployments" tab
   - Click "Redeploy" to apply CORS changes

## ✅ Step 3: Verify Connection

1. **Test Backend:**
   - Open: `https://pakistani-project-backend.up.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Test Frontend:**
   - Open your Netlify URL
   - Open browser console (F12)
   - Check for any CORS errors

3. **Test API Connection:**
   - Try to register/login from the frontend
   - Check browser console for API calls

## 📝 Environment Variables Summary

### Railway Backend Variables:
```
DATABASE_URL=auto-set-by-railway
ELEVENLABS_API_KEY=your_key
EASYPAY_API_KEY=your_key
EASYPAY_MERCHANT_ID=your_id
EASYPAY_STORE_ID=your_id
CLAID_API_KEY=your_key
JWT_SECRET=your_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=https://your-netlify-app.netlify.app
BACKEND_URL=https://pakistani-project-backend.up.railway.app
NETLIFY_URL=https://your-netlify-app.netlify.app
```

### Netlify Frontend Variables (if using GitHub deployment):
```
VITE_API_URL=https://pakistani-project-backend.up.railway.app
```

## 🎯 Quick Checklist

- [ ] Deploy `frontend/dist` to Netlify (drag & drop or GitHub)
- [ ] Get Netlify URL
- [ ] Update Railway `FRONTEND_URL` with Netlify URL
- [ ] Update Railway `BACKEND_URL` with Railway URL
- [ ] Redeploy Railway to apply CORS changes
- [ ] Test frontend → backend connection
- [ ] Verify API calls work from frontend

## 🐛 Troubleshooting

### CORS Errors
- **Symptom:** Browser console shows CORS errors
- **Fix:** Make sure `FRONTEND_URL` is set in Railway with your Netlify URL
- **Fix:** Redeploy Railway after setting environment variables

### API Not Found (404)
- **Symptom:** Frontend can't reach backend
- **Fix:** Check `VITE_API_URL` is set correctly in Netlify
- **Fix:** If using drag & drop, the build already has the Railway URL baked in

### Environment Variable Not Working
- **Symptom:** Frontend still uses `http://localhost:8000`
- **Fix:** If using drag & drop, rebuild with: `$env:VITE_API_URL="https://pakistani-project-backend.up.railway.app"; npm run build`
- **Fix:** If using GitHub, set `VITE_API_URL` in Netlify environment variables

## 📦 Your Build File Location

**Ready to deploy:** `frontend/dist/`

Just drag and drop this folder to Netlify!

