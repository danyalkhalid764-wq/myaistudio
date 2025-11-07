# Quick Start Guide - Push to GitHub and Deploy to Railway

## Step 1: Install Git

**Git is not currently installed on your system.**

1. Download Git from: https://git-scm.com/download/win
2. Run the installer with default settings
3. **Restart PowerShell** after installation
4. Verify installation by running: `git --version`

## Step 2: Run Setup Script

After installing Git and restarting PowerShell, run:

```powershell
.\setup_git_and_push.ps1
```

This script will:
- Configure Git with your email (danyalkhalid764@gmail.com)
- Initialize the Git repository
- Create the initial commit
- Guide you through connecting to GitHub

## Step 3: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Name your repository (e.g., "myaistudio" or "pakistaniproject")
4. Choose Public or Private
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click "Create repository"

## Step 4: Connect and Push to GitHub

After creating the repository, GitHub will show you commands. Or run:

```powershell
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**Note:** When pushing, GitHub will ask for authentication:
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your GitHub password)

### Create Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Copy the token and use it as your password

## Step 5: Deploy Backend to Railway

1. Go to https://railway.app and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect the backend automatically

### Add PostgreSQL Database:
1. In Railway project, click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically sets `DATABASE_URL`

### Set Environment Variables:
In Railway → Variables, add:

```
ELEVENLABS_API_KEY=your_key_here
CLAID_API_KEY=your_key_here
EASYPAY_API_KEY=your_key_here
EASYPAY_MERCHANT_ID=your_merchant_id
EASYPAY_STORE_ID=your_store_id
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NETLIFY_URL=https://your-netlify-app.netlify.app
```

### Configure Service:
1. Go to your service settings
2. Set **Root Directory** to `backend`
3. Railway will automatically use the Procfile

### Get Your Railway URL:
After deployment, Railway provides a URL like: `https://your-app.up.railway.app`

## Step 6: Update Netlify Frontend

1. In Netlify, go to Site settings → Environment variables
2. Add/Update: `VITE_API_URL` or `REACT_APP_API_URL` with your Railway URL
3. Redeploy your Netlify site

## Troubleshooting

### Git not found after installation:
- Restart PowerShell completely
- Check if Git is in PATH: `$env:Path`

### Authentication failed:
- Use Personal Access Token, not password
- Make sure token has `repo` permissions

### Railway deployment fails:
- Check Railway logs
- Verify all environment variables are set
- Ensure Root Directory is set to `backend`

## Files Created for You

- ✅ `.gitignore` - Excludes sensitive files
- ✅ `Procfile` - Railway deployment command
- ✅ `railway.json` - Railway configuration
- ✅ `RAILWAY_DEPLOYMENT.md` - Detailed Railway guide
- ✅ `GITHUB_SETUP.md` - Detailed GitHub guide
- ✅ `setup_git_and_push.ps1` - Automated setup script

## Need Help?

If you encounter issues:
1. Check the detailed guides: `RAILWAY_DEPLOYMENT.md` and `GITHUB_SETUP.md`
2. Check Railway logs for deployment errors
3. Verify all environment variables are set correctly

