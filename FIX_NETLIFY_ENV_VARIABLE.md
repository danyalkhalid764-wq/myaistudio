# Fix: VITE_API_URL Undefined Error

## 🔴 Problem
- `VITE_API_URL env var: undefined`
- Frontend defaults to `http://localhost:8000`
- Requests timeout because localhost doesn't exist in production

## ✅ Solution: Set VITE_API_URL in Netlify

### Step 1: Get Your Railway Backend URL
1. Go to Railway dashboard
2. Find your backend service
3. Copy the public URL (e.g., `https://pakistani-project-backend.up.railway.app`)

### Step 2: Set Environment Variable in Netlify

**Option A: If Using Git-Based Deployment (Recommended)**

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Select your site
3. Click **Site settings** (gear icon)
4. Click **Environment variables** (left sidebar)
5. Click **Add a variable**
6. Enter:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-railway-backend.railway.app` (your actual Railway URL)
   - **Scopes**: Select "All scopes" or "Production"
7. Click **Save**

8. **Trigger a New Build**:
   - Go to **Deploys** tab
   - Click **Trigger deploy** → **Deploy site**
   - Netlify will rebuild with the environment variable

**Option B: If Using Drag-and-Drop Deployment**

1. Set the environment variable in Netlify (steps 1-7 above)
2. **Rebuild locally**:
   ```bash
   cd frontend
   npm run build
   ```
3. **Upload the new `dist` folder** to Netlify

**⚠️ Important**: For drag-and-drop, you need to set the variable in Netlify first, then rebuild locally. The variable won't be available during local build, but you can set it in Netlify and then use Git-based deployment instead.

### Step 3: Verify It's Working

After the new build:

1. Open your Netlify site
2. Open browser console (F12)
3. Try to login/register
4. Check console - you should see:
   ```
   🔗 API Base URL: https://your-railway-backend.railway.app ✅
   🔗 VITE_API_URL env var: https://your-railway-backend.railway.app ✅
   ```

## 🚀 Recommended: Switch to Git-Based Deployment

If you're using drag-and-drop, switch to Git-based deployment:

1. **Connect GitHub repo to Netlify**:
   - In Netlify: **Add new site** → **Import an existing project**
   - Connect your GitHub repo
   - Set build settings:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`

2. **Set environment variable** (as shown above)

3. **Deploy**: Netlify will build automatically on every push

## 📋 Quick Checklist

- [ ] Got Railway backend URL
- [ ] Set `VITE_API_URL` in Netlify environment variables
- [ ] Value is your Railway URL (starts with `https://`)
- [ ] Triggered new build (Git-based) OR rebuilt and uploaded (drag-and-drop)
- [ ] Verified in browser console that API URL is correct (not localhost:8000)

## 🔧 If Still Not Working

1. **Check variable name**: Must be exactly `VITE_API_URL` (case-sensitive)
2. **Check variable scope**: Set for "Production" or "All scopes"
3. **Check build logs**: In Netlify Deploys tab, check if build succeeded
4. **Clear browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
5. **Check Railway backend**: Make sure it's running and accessible

