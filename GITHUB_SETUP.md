# GitHub Setup and Push Guide

This guide will help you push your code to GitHub.

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Install with default settings
   - Restart your terminal/PowerShell after installation

2. **GitHub Account**: Make sure you have a GitHub account

## Step 1: Install Git

If Git is not installed:
1. Go to https://git-scm.com/download/win
2. Download the Windows installer
3. Run the installer with default settings
4. Restart your terminal/PowerShell

## Step 2: Configure Git (First Time Only)

After installing Git, configure it with your information:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## Step 3: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name your repository (e.g., "myaistudio" or "pakistaniproject")
5. Choose public or private
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 4: Initialize Git Repository

Open PowerShell in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: MyAIStudio project"

# Add remote repository (replace with your GitHub repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 5: Authentication

When you push, GitHub will ask for authentication. You have two options:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` permissions
3. Use the token as your password when pushing

### Option B: GitHub CLI
1. Install GitHub CLI: https://cli.github.com/
2. Run `gh auth login`
3. Follow the prompts

## Step 6: Verify Push

1. Go to your GitHub repository
2. Verify all files are uploaded
3. Check that sensitive files (like `.env`) are NOT in the repository

## Important Notes

- **Never commit `.env` files** - They contain sensitive information
- The `.gitignore` file is already configured to exclude:
  - `.env` files
  - `venv/` directories
  - `node_modules/`
  - `__pycache__/`
  - `generated_videos/`
  - `tmp_uploads/`

## Troubleshooting

### Git not found
- Make sure Git is installed
- Restart your terminal after installation
- Check if Git is in your PATH

### Authentication failed
- Use Personal Access Token instead of password
- Make sure your token has `repo` permissions

### Push rejected
- Make sure you've committed your changes first
- Check if the remote repository exists
- Verify your repository URL is correct

