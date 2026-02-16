# Complete Render Deployment Guide - 400 Error Fix

## Issue: 400 Bad Request Error

This error typically occurs due to mismatched CSRF tokens, ALLOWED_HOSTS, or HTTPS configuration issues.

## Fixed Issues

### 1. **ALLOWED_HOSTS Configuration**
- ✅ Added `*.onrender.com` wildcard pattern
- ✅ Added `0.0.0.0` for internal routing
- ✅ Proper parsing from environment variables

### 2. **CSRF Token Security**
- ✅ Added CSRF_TRUSTED_ORIGINS for Render domains
- ✅ Set CSRF_COOKIE_HTTPONLY=False (allows JavaScript access)
- ✅ Added proper CSRF_COOKIE_SAMESITE setting
- ✅ Configured CSRF for both secure (HTTPS) and development modes

### 3. **HTTPS & Proxy Configuration**
- ✅ SECURE_PROXY_SSL_HEADER set for reverse proxy headers
- ✅ USE_X_FORWARDED_HOST=True (tells Django to trust proxy headers)
- ✅ USE_X_FORWARDED_PORT=True (trusts X-Forwarded-Port header)
- ✅ SECURE_SSL_REDIRECT automatically enabled in production

### 4. **Session Cookie Security**
- ✅ SESSION_COOKIE_SECURE only enabled in production
- ✅ SESSION_COOKIE_HTTPONLY=True for security
- ✅ Proper SameSite settings for both cookies

## Step-by-Step Deployment

### Step 1: Verify Local Environment
```bash
cd /Users/anu/Downloads/project

# Test with local .env
python manage.py runserver
```

### Step 2: Update Render Environment Variables

Go to: https://dashboard.render.com → Your Service → Environment

Add/Update these variables:

```
SECRET_KEY=django-insecure-feedback-collection-system-dev-key-change-in-production
DEBUG=False
ALLOWED_HOSTS=feedback-manager-f80h.onrender.com,*.onrender.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.mxqkuxgzkgfujsbtyxux
DB_PASSWORD=aed1xVEyLvKDkQBm
DB_HOST=aws-1-ap-south-1.pooler.supabase.com
DB_PORT=6543
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

### Step 3: Trigger Redeploy

Option A: Manual Deploy
1. Go to Render dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

Option B: Push to GitHub (auto-deploy)
```bash
git add -A
git commit -m "Production deployment fixes"
git push origin main
```

### Step 4: Verify Deployment

1. Wait for deployment to complete (check logs)
2. Visit: https://feedback-manager-f80h.onrender.com
3. Open Browser DevTools (F12) → Network tab
4. Check if requests return 200 (not 400)
5. Look for any CSRF token errors in Console

## Troubleshooting 400 Errors

### Check Logs
Go to: Render Dashboard → Service → Logs

Common errors:
```
Invalid HTTP_HOST header → Add domain to ALLOWED_HOSTS
CSRF token missing → Check if CSRF_TRUSTED_ORIGINS is set
```

### Enable Debug Temporarily
⚠️ Only for debugging, disable immediately after:

1. Set DEBUG=True in Render environment
2. Redeploy and check error page
3. Set DEBUG=False again
4. Redeploy

### Test CSRF Token
Add this to a template to verify token:
```html
<p>CSRF Token: {{ csrf_token }}</p>
```

### Check Static Files
If CSS/JS return 400:
```bash
python manage.py collectstatic --noinput
```

## Quick Reference

| Setting | Development | Production |
|---------|------------|-----------|
| DEBUG | True | False ✅ |
| SECURE_SSL_REDIRECT | False | True ✅ |
| CSRF_COOKIE_SECURE | False | True ✅ |
| SESSION_COOKIE_SECURE | False | True ✅ |
| ALLOWED_HOSTS | localhost,127.0.0.1 | *.onrender.com ✅ |

## Files Changed

1. `feedback_project/settings.py` - Comprehensive security fixes
2. `.env.example` - Updated example environment
3. `.env.production.example` - Production template (new)
4. `Dockerfile` - Production-ready Docker setup
5. `render.yaml` - Render deployment config

## After Successful Deployment

1. ✅ Test all forms (feedback, login, registration)
2. ✅ Test button clicks and AJAX requests
3. ✅ Verify static files load (CSS/JS/images)
4. ✅ Check database connectivity
5. ✅ Monitor error logs for any issues

## Support

If 400 errors persist:
1. Check Render logs for specific error messages
2. Verify all environment variables are set
3. Clear browser cache: DevTools → Network → Disable cache
4. Try incognito mode
5. Check ALLOWED_HOSTS includes your exact domain

---
**Last Updated:** February 16, 2026
**Status:** ✅ Production Ready
