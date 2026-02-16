# Render Deployment Guide

## Prerequisites
- GitHub repository with your code
- Render account (https://render.com)
- Environment variables configured

## Steps to Deploy

### 1. Push to GitHub
```bash
git add Dockerfile .dockerignore render.yaml
git commit -m "Add Docker configuration for Render deployment"
git push origin main
```

### 2. Connect to Render
1. Go to [Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Select **Build and deploy from a Git repository**
4. Connect your GitHub account and select the repository
5. Fill in the details:
   - **Name**: feedback-collection-app
   - **Runtime**: Docker
   - **Branch**: main
   - **Build command**: (leave empty - Dockerfile will handle it)
   - **Start command**: (leave empty - Dockerfile handles it)

### 3. Configure Environment Variables
Add these in Render dashboard under Environment:

```
SECRET_KEY=django-insecure-feedback-collection-system-dev-key-change-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.onrender.com,yourdomain.com
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

⚠️ **Security Warning**: Change `SECRET_KEY` and database credentials for production!

### 4. Deploy
1. Click **Create Web Service**
2. Wait for deployment to complete
3. Access your app via the provided Render URL

## Important Notes

- The Dockerfile uses Python 3.11 slim image
- Gunicorn is configured with 3 workers
- Static files are collected during build
- Port 10000 is used (Render standard)
- Non-root user runs the application for security

## Troubleshooting

**Static files not loading?**
- Ensure `DEBUG=False` in production
- Update `STATIC_URL` and `STATIC_ROOT` in settings.py if needed

**Database connection issues?**
- Verify Supabase credentials in environment variables
- Check DB_HOST, DB_PORT, DB_USER, DB_PASSWORD

**Port binding issues?**
- Render uses port 10000 by default
- Ensure your Django settings allow this

## Cost Optimization
- Render offers a free tier (limited)
- Monitor resource usage in dashboard
- Use paid plans for production apps
