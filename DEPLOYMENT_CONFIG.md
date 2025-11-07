# Deployment Configuration Guide

## Overview
This document outlines all the environment variables and configurations needed for deploying the frontend to Netlify and backend to Railway.

## Backend (Railway) Configuration

### Required Environment Variables

1. **Database**
   - `DATABASE_URL` - PostgreSQL connection string (Railway provides this automatically if you add a PostgreSQL service)

2. **API Keys**
   - `ELEVENLABS_API_KEY` - Your ElevenLabs API key
   - `EASYPAY_API_KEY` - Your Easypaisa API key
   - `EASYPAY_MERCHANT_ID` - Your Easypaisa merchant ID
   - `EASYPAY_STORE_ID` - Your Easypaisa store ID
   - `CLAID_API_KEY` - Your Claid API key

3. **JWT Settings**
   - `JWT_SECRET` - Secret key for JWT tokens (use a strong random string)
   - `JWT_ALGORITHM` - JWT algorithm (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

4. **URLs (IMPORTANT for production)**
   - `FRONTEND_URL` - Your Netlify frontend URL (e.g., `https://your-app.netlify.app`)
   - `BACKEND_URL` - Your Railway backend URL (e.g., `https://your-app.railway.app`)

5. **CORS Settings (Optional)**
   - `NETLIFY_URL` - Your Netlify URL (alternative to FRONTEND_URL)
   - `CORS_ALLOW_ALL` - Set to `true` to allow all origins (not recommended for production)

### Railway Setup Steps

1. Connect your GitHub repository to Railway
2. Add a PostgreSQL service
3. Set all environment variables in Railway dashboard
4. Deploy the backend

## Frontend (Netlify) Configuration

### Required Environment Variables

1. **API URL**
   - `VITE_API_URL` - Your Railway backend URL (e.g., `https://your-app.railway.app`)

### Netlify Setup Steps

1. Drag and drop the `frontend/dist` folder to Netlify, OR
2. Connect your GitHub repository and set build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Set `VITE_API_URL` environment variable in Netlify dashboard
4. Deploy

## Endpoint Configuration Summary

### Backend Endpoints (Railway)
- Base URL: `https://your-app.railway.app`
- Authentication: `/auth/*`
- TTS API: `/api/*`
- Payments: `/api/payment/*`
- Video: `/api/video/*`
- Static Videos: `/static/videos/*`

### Frontend Endpoints (Netlify)
- Base URL: `https://your-app.netlify.app`
- All API calls use `VITE_API_URL` environment variable

## Important Notes

1. **CORS Configuration**: The backend automatically adds your `FRONTEND_URL` to allowed origins
2. **Payment URLs**: Payment return/cancel/callback URLs are automatically configured based on `FRONTEND_URL` and `BACKEND_URL`
3. **Environment Variables**: Make sure to set all required environment variables before deploying
4. **Build**: Frontend must be built with `npm run build` before deploying to Netlify

## Testing After Deployment

1. Check backend health: `https://your-backend.railway.app/health`
2. Check frontend loads: `https://your-frontend.netlify.app`
3. Test API connection from frontend
4. Verify CORS is working (check browser console)

