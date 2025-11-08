# Fix: Environment Variable Not Working in Netlify

## 🔴 Problem
- `API Base URL: http://localhost:8000` ❌
- `VITE_API_URL env var: undefined` ❌
- Requests timing out

## ✅ Solution: Check These Steps

### Step 1: Verify Environment Variable is Set

1. Go to **Netlify Dashboard** → Your site
2. **Site settings** → **Environment variables**
3. **Check if `VITE_API_URL` exists**:
   - Should see: `VITE_API_URL` = `https://pakistani-project-backend-production.up.railway.app`
   - If not there → Add it
   - If wrong value → Update it

### Step 2: Check Variable Name (Case-Sensitive!)

⚠️ **CRITICAL**: The variable name must be **exactly** `VITE_API_URL`
- ✅ Correct: `VITE_API_URL`
- ❌ Wrong: `VITE_API_url`, `vite_api_url`, `VITE-API-URL`, etc.

### Step 3: Check Variable Scope

Make sure the variable is set for the correct scope:
- **Production** (recommended)
- Or **All scopes**

### Step 4: Trigger a NEW Build

**IMPORTANT**: After setting/updating the variable, you MUST trigger a new build:

1. Go to **Deploys** tab
2. Click **Trigger deploy** → **Deploy site**
3. Wait for build to complete (2-5 minutes)

### Step 5: Clear Browser Cache

After the new build:
1. **Hard refresh** your browser:
   - Windows: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`
2. Or **clear browser cache** completely

## 🔍 How to Verify It's Working

After triggering a new build:

1. **Open your Netlify site**
2. **Open browser console** (F12)
3. **Check console** - You should see:
   ```
   🔗 API Base URL: https://pakistani-project-backend-production.up.railway.app ✅
   🔗 VITE_API_URL env var: https://pakistani-project-backend-production.up.railway.app ✅
   ```

If you still see `localhost:8000`, the variable is not set correctly or the build didn't pick it up.

## 📋 Troubleshooting Checklist

- [ ] `VITE_API_URL` exists in Netlify environment variables
- [ ] Variable name is exactly `VITE_API_URL` (case-sensitive)
- [ ] Value is: `https://pakistani-project-backend-production.up.railway.app`
- [ ] Variable scope is set correctly (Production or All scopes)
- [ ] Triggered a NEW build after setting/updating the variable
- [ ] Build completed successfully
- [ ] Cleared browser cache / hard refreshed
- [ ] Checked console - still shows localhost? → Variable not set correctly

## 🚨 Common Mistakes

1. **Variable name typo**: `VITE_API_URL` vs `VITE-API-URL` vs `vite_api_url`
2. **Forgot to trigger new build**: Variable set but old build still active
3. **Wrong scope**: Variable set for wrong environment
4. **Browser cache**: Old JavaScript still cached

## ✅ Quick Fix Steps

1. **Double-check** `VITE_API_URL` in Netlify environment variables
2. **Delete and re-add** the variable if unsure
3. **Trigger a new build** (Deploys tab → Trigger deploy)
4. **Wait for build** to complete
5. **Hard refresh** browser (Ctrl+Shift+R)
6. **Test again**

