# How to Redeploy/Trigger New Build in Netlify

## 🔍 Where to Find the Redeploy Option

### Method 1: From Deploys Tab (Easiest)

1. **Go to your Netlify site dashboard**
   - Visit: https://app.netlify.com/
   - Click on your site

2. **Click on "Deploys" tab** (top navigation)
   - You'll see a list of your deployments

3. **Look for "Trigger deploy" button**
   - It's usually at the top right of the Deploys page
   - Or click the three dots (⋯) menu next to your site name
   - Select **"Trigger deploy"** → **"Deploy site"**

### Method 2: From Site Overview

1. **Go to your site dashboard**
2. **Look for the "Deploys" section** on the main page
3. **Click "Trigger deploy"** button (usually visible on the right side)

### Method 3: From Site Settings

1. **Go to Site settings** (gear icon)
2. **Click "Build & deploy"** (left sidebar)
3. **Scroll down to "Deploy settings"**
4. **Click "Trigger deploy"** button

### Method 4: Push a New Commit (Automatic)

If your site is connected to GitHub:
1. Make a small change (like adding a comment)
2. Commit and push to GitHub
3. Netlify will automatically rebuild

## 📋 Step-by-Step Visual Guide

1. **Netlify Dashboard** → Your site
2. **Top navigation** → Click **"Deploys"** tab
3. **Top right corner** → Click **"Trigger deploy"** button
4. **Dropdown menu** → Select **"Deploy site"**
5. **Wait** for build to complete (2-5 minutes)

## ⚠️ Important Notes

- **After setting environment variable**, you MUST trigger a new build
- The variable is only included at **build time**, not runtime
- Build will show in the Deploys list with a status (Building → Published)

## 🔍 Can't Find It?

If you still can't find the "Trigger deploy" button:

1. **Check if you're on the right page**: Make sure you're in the **Deploys** tab
2. **Look for three dots menu** (⋯) - it might be there
3. **Try refreshing the page** - sometimes UI needs a refresh
4. **Check permissions** - make sure you have deploy permissions for the site

## ✅ After Triggering Deploy

1. You'll see a new deployment appear in the list
2. Status will show: "Building..." → "Published"
3. Once published, test your site
4. Check browser console to verify API URL is correct

