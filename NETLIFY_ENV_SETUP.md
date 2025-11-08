# How to Set VITE_API_URL in Netlify

## ⚠️ IMPORTANT: Vite Environment Variables Must Be Set at BUILD Time

Vite environment variables (those starting with `VITE_`) are embedded into the build at **build time**, not runtime. This means:

1. ✅ Set the variable in Netlify **before** building
2. ✅ Or trigger a **new build** after setting the variable

## 📋 Step-by-Step Instructions

### Method 1: Set in Netlify Dashboard (Recommended)

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com/
   - Select your site

2. **Navigate to Environment Variables**
   - Click: **Site settings** (gear icon)
   - Click: **Environment variables** (in left sidebar)

3. **Add New Variable**
   - Click: **Add a variable** button
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-railway-backend.railway.app`
     - Replace with your actual Railway backend URL
     - Example: `https://pakistani-project-backend.up.railway.app`
   - **Scopes**: Select "All scopes" (or specific scopes if needed)
   - Click: **Save**

4. **Trigger a New Build**
   - Go to: **Deploys** tab
   - Click: **Trigger deploy** → **Deploy site**
   - Or push a new commit to trigger auto-deploy

### Method 2: Set in netlify.toml (For Git-based Deploys)

If you want to set it in code (not recommended for production URLs):

```toml
[build.environment]
  NODE_VERSION = "18"
  VITE_API_URL = "https://your-railway-backend.railway.app"
```

⚠️ **Warning**: Don't commit production URLs to Git. Use Netlify Dashboard instead.

## ✅ Verify It's Working

After setting the variable and rebuilding:

1. **Open your Netlify site**
2. **Open browser console** (F12)
3. **Try to login/register**
4. **Check console** - You should see:
   ```
   🔗 API Base URL: https://your-railway-backend.railway.app ✅
   🔗 VITE_API_URL env var: https://your-railway-backend.railway.app ✅
   ```

If you still see:
```
🔗 API Base URL: http://localhost:8000 ❌
🔗 VITE_API_URL env var: undefined ❌
```

Then the variable is not set correctly or the build didn't pick it up.

## 🔧 Troubleshooting

### Issue: Variable set but still showing undefined

**Solution**: 
- Make sure variable name is exactly: `VITE_API_URL` (case-sensitive)
- Trigger a new build after setting the variable
- Check that the variable is set for the correct scope (production/preview)

### Issue: Build fails

**Solution**:
- Make sure the Railway URL is correct and accessible
- Test the URL: `https://your-railway-backend.railway.app/health`
- Should return: `{"status": "healthy"}`

### Issue: Still getting timeout errors

**Solution**:
- Verify Railway backend is running
- Check CORS configuration in backend
- Make sure Railway URL is correct (starts with `https://`)

## 📝 Quick Checklist

- [ ] `VITE_API_URL` is set in Netlify environment variables
- [ ] Value is your Railway backend URL (starts with `https://`)
- [ ] New build has been triggered after setting the variable
- [ ] Browser console shows the correct API URL (not localhost:8000)
- [ ] Railway backend is running and accessible

