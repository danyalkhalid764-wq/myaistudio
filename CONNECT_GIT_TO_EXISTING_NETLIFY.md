# Connect GitHub Repo to Existing Netlify Site

## 🔄 Switch from Manual Deployment to Git-Based Deployment

You currently have a Netlify site deployed via drag-and-drop (dist folder). Here's how to connect your GitHub repo to it.

## 📋 Step-by-Step Instructions

### Step 1: Go to Your Existing Netlify Site

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Click on your existing site (the one deployed with dist folder)

### Step 2: Connect GitHub Repository

1. Go to **Site settings** (gear icon)
2. Click **Build & deploy** (left sidebar)
3. Scroll down to **"Continuous Deployment"** section
4. Click **"Link to Git provider"** or **"Connect to Git"** button
5. Select **GitHub** (authorize if needed)
6. Select your repository: **`myaistudio-frontend`**
7. Click **"Save"**

### Step 3: Configure Build Settings

After connecting, configure:

- **Base directory**: (leave empty - root is fine)
- **Build command**: `npm run build`
- **Publish directory**: `dist`
- **Node version**: 18

These should auto-detect from `netlify.toml`, but verify them.

### Step 4: Set Environment Variable (If Not Already Set)

1. Go to **Site settings** → **Environment variables**
2. Add or update:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://pakistani-project-backend-production.up.railway.app`
3. Click **Save**

### Step 5: Trigger First Build from Git

1. Go to **Deploys** tab
2. Click **Trigger deploy** → **Deploy site**
3. Or push a new commit to trigger auto-deploy

## ✅ What Happens Next

- **Old deployment** (from dist folder): Will remain in deploy history but won't be used
- **New deployment** (from Git): Will be the active deployment
- **Future updates**: Just push to GitHub, Netlify will auto-deploy

## 🔄 Benefits of Git-Based Deployment

✅ **Automatic builds** when you push to GitHub
✅ **Environment variables** work correctly
✅ **Build logs** show in Netlify
✅ **Easy rollback** to previous deployments
✅ **No need to manually upload dist folder**

## 📝 Important Notes

- Your existing site URL won't change
- The old dist-based deployment will be replaced by Git-based deployment
- Make sure `VITE_API_URL` is set before the first Git build
- After connecting Git, all future deployments will be from GitHub

## 🎯 Quick Checklist

- [ ] Connected GitHub repo to existing Netlify site
- [ ] Build settings configured (from netlify.toml)
- [ ] `VITE_API_URL` environment variable set
- [ ] Triggered first build from Git
- [ ] Build completed successfully
- [ ] Tested site - login/register works

## 🚀 After Setup

Once connected:
- **Push to GitHub** → Netlify auto-deploys
- **Set environment variables** → They're included in builds
- **No more manual uploads** needed!

