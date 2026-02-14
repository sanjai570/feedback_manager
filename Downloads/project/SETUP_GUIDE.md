# Setup and Deployment Instructions

This is a comprehensive guide to set up and run the Feedback Collection System locally and deploy it to production.

## Table of Contents
1. Prerequisites
2. Local Development Setup
3. Supabase Configuration
4. Running the Application
5. Creating Admin Account
6. Database Management
7. Deployment Guide
8. Troubleshooting

---

## Prerequisites

- **Python 3.10 or higher**
- **PostgreSQL** (or Supabase)
- **Git**
- **Virtual Environment** (venv or conda)
- **pip** (Python package manager)

---

## Local Development Setup

### Step 1: Clone the Project

```bash
cd /Users/anu/Downloads/project
```

### Step 2: Create Virtual Environment

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password
DB_HOST=your-project.supabase.co
DB_PORT=5432

# Security Settings (keep False for development)
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
```

---

## Supabase Configuration

### Step 1: Create Supabase Project

1. Visit [supabase.com](https://supabase.com/)
2. Sign up or log in
3. Create a new project
4. Save your project URL and database password

### Step 2: Get Database Credentials

1. Go to Project Settings → Database
2. Copy the following:
   - Host: `db.{project-id}.supabase.co`
   - Username: `postgres`
   - Password: (provided during setup)
   - Database: `postgres`
   - Port: `5432`

### Step 3: Update .env File

Update your `.env` file with these credentials:

```env
DB_HOST=db.xxxxx.supabase.co
DB_PASSWORD=your-password-here
```

---

## Running the Application

### Step 1: Run Migrations

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, feedback_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ... (more migrations)
  Applying feedback_app.0001_initial... OK
```

### Step 2: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 3: Run Development Server

```bash
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000/**

---

## Creating Admin Account

### Method 1: Interactive Command

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: (enter secure password)
Password (again): (confirm password)
Superuser created successfully.
```

### Method 2: Management Command Script

Create a file `create_admin.py`:

```python
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'SecurePassword123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✓ Admin user '{username}' created successfully!")
else:
    print(f"✗ User '{username}' already exists!")
```

Run it:
```bash
python manage.py shell < create_admin.py
```

### Method 3: Django Admin Panel

1. Log in to admin panel: `http://localhost:8000/admin/`
2. Create a new user with staff and superuser privileges

---

## Database Management

### Viewing Database

#### Option 1: Django Admin Panel
```
URL: http://localhost:8000/admin/
Login with admin credentials
Navigate to "Feedback" section
```

#### Option 2: Supabase Dashboard
```
Visit https://supabase.com/dashboard
Navigate to your project
Go to SQL Editor or Table Editor
```

### Backup Database

```bash
# Export data
python manage.py dumpdata feedback_app.Feedback > feedback_backup.json

# Export specific model
python manage.py dumpdata feedback_app.Feedback --format json > feedback_data.json
```

### Restore Database

```bash
# Restore from backup
python manage.py loaddata feedback_backup.json
```

### Reset Database (DANGEROUS - Deletes all data)

```bash
# Delete all migrations
rm feedback_app/migrations/0*.py
touch feedback_app/migrations/__init__.py

# Recreate migrations
python manage.py makemigrations

# Migrate fresh
python manage.py migrate
```

---

## Project Structure

```
project/
│
├── feedback_project/          # Django project config
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI config
│   └── asgi.py                # ASGI config
│
├── feedback_app/              # Main application
│   ├── models.py              # Database models
│   ├── views.py               # Business logic
│   ├── forms.py               # Django forms
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Admin panel config
│   ├── migrations/            # Database migrations
│   └── tests.py               # Unit tests
│
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   ├── feedback_form.html      # Student feedback form
│   ├── dashboard.html          # Admin dashboard
│   ├── login.html              # Admin login
│   ├── feedback_management.html # Feedback management
│   └── confirm_delete.html      # Delete confirmation
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css          # Modern styling
│   └── js/
│       └── script.js           # Interactive features
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

---

## Features Implemented

### Student Side
- ✅ Modern feedback submission form
- ✅ Client-side and server-side validation
- ✅ Rating system (1-5 stars)
- ✅ Anonymous submission option
- ✅ Success notification
- ✅ Mobile responsive design

### Admin Side
- ✅ Secure login system
- ✅ Dashboard with statistics
- ✅ Feedback management page
- ✅ Search functionality
- ✅ Filter by department and rating
- ✅ Pagination support
- ✅ Delete feedback option
- ✅ Rating distribution chart
- ✅ Department-wise stats

### Technical Features
- ✅ Django ORM for database operations
- ✅ Supabase PostgreSQL integration
- ✅ CSRF protection enabled
- ✅ User authentication
- ✅ Responsive design (mobile & desktop)
- ✅ Toast notifications
- ✅ Empty state design
- ✅ Chart visualization
- ✅ Environment configuration

---

## Deployment Guide

### Deploy to Heroku

1. **Create Heroku Account** and install Heroku CLI

2. **Create Procfile**:
```
web: gunicorn feedback_project.wsgi
```

3. **Update settings.py for production**:
```python
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

4. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to PythonAnywhere

1. Visit [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Create account and upload code
3. Configure virtual environment
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Configure web app settings

### Deploy to AWS/DigitalOcean

Use Gunicorn + Nginx:

```bash
gunicorn feedback_project.wsgi:application --bind 0.0.0.0:8000
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution**:
```bash
pip install -r requirements.txt
source venv/bin/activate  # macOS/Linux
```

### Issue: "psycopg2: error: could not translate host name"

**Solution**: Check Supabase database credentials in `.env`:
```bash
# Make sure DB_HOST is correct
DB_HOST=db.xxxxx.supabase.co
```

### Issue: "Permission denied: '/static/'"

**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

### Issue: "CSRF token missing or incorrect"

**Solution**: Ensure `{{ csrf_token }}` is in forms:
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Issue: Admin panel not loading

**Solution**: Migrate database:
```bash
python manage.py migrate
```

---

## Performance Tips

1. **Enable Caching**:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

2. **Use Database Indexing**:
```python
class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

3. **Optimize Queries**:
```python
feedbacks = Feedback.objects.select_related().prefetch_related()
```

4. **Enable GZIP Compression**:
```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware
]
```

---

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG = False` in production
- [ ] Use `HTTPS` in production
- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Use strong admin password
- [ ] Enable `CSRF_COOKIE_SECURE`
- [ ] Use environment variables for secrets
- [ ] Regular database backups
- [ ] Keep dependencies updated

---

## Support & Contact

For issues or questions:
1. Check troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Supabase docs: https://supabase.com/docs

---

**Last Updated**: February 2026
**Version**: 1.0.0
**License**: MIT
