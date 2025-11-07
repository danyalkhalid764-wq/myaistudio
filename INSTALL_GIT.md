# Install Git - Quick Guide

## Step 1: Download Git

1. Go to: **https://git-scm.com/download/win**
2. Click the download button for Windows
3. The download will start automatically

## Step 2: Install Git

1. Run the downloaded installer (e.g., `Git-2.43.0-64-bit.exe`)
2. Click "Next" through the installation wizard
3. **Use default settings** (recommended)
4. Click "Install"
5. Wait for installation to complete
6. Click "Finish"

## Step 3: Restart PowerShell

**IMPORTANT:** After installing Git, you MUST restart PowerShell:

1. Close your current PowerShell window
2. Open a new PowerShell window
3. Navigate back to your project:
   ```powershell
   cd d:\pakistaniproject
   ```

## Step 4: Verify Installation

Run this command to verify Git is installed:

```powershell
git --version
```

You should see something like: `git version 2.43.0.windows.1`

## Step 5: Push to GitHub

Once Git is installed and PowerShell is restarted, run:

```powershell
.\push_to_github.ps1
```

This script will:
- Configure Git with your email (danyalkhalid764@gmail.com)
- Initialize the repository
- Add all files
- Create the initial commit
- Push to: https://github.com/danyalkhalid764-wq/myaistudio.git

## Alternative: Manual Commands

If you prefer to run commands manually:

```powershell
# Configure Git
git config --global user.email "danyalkhalid764@gmail.com"
git config --global user.name "Your Name"

# Initialize repository
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: MyAIStudio project with Railway deployment setup"

# Add remote
git remote add origin https://github.com/danyalkhalid764-wq/myaistudio.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Authentication

When pushing, GitHub will ask for credentials:

- **Username:** `danyalkhalid764-wq`
- **Password:** Use a **Personal Access Token** (NOT your GitHub password)

### Create Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: "MyAIStudio Push"
4. Select scope: **`repo`** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

## Troubleshooting

### "git is not recognized"
- Git is not installed or not in PATH
- Restart PowerShell after installation
- Check if Git is installed: `where git`

### "Authentication failed"
- Use Personal Access Token, not password
- Make sure token has `repo` permissions
- Token might have expired (create a new one)

### "Permission denied"
- Check repository URL is correct
- Verify you have write access to the repository
- Make sure you're using the correct GitHub account

## Need Help?

If you encounter issues:
1. Check that Git is installed: `git --version`
2. Verify repository URL is correct
3. Make sure you have a Personal Access Token
4. Check your internet connection




