# Quick Reference Guide

## Project Quick Start (TL;DR)

### Setup (5 minutes)

```bash
# 1. Clone/Navigate to project
cd /Users/anu/Downloads/project

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your Supabase credentials

# 5. Migrate database
python manage.py migrate

# 6. Create admin account
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

### Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Student feedback form |
| `http://localhost:8000/admin/login/` | Admin login |
| `http://localhost:8000/admin/dashboard/` | Admin dashboard |
| `http://localhost:8000/admin/feedback/` | Feedback list & manage |
| `http://localhost:8000/admin/` | Django admin panel |

---

## Supabase Setup (10 minutes)

1. Visit https://supabase.com
2. Create new project
3. Get database credentials:
   - Host: `db.xxxxx.supabase.co`
   - User: `postgres`
   - Password: (your password)
   - Database: `postgres`
   - Port: `5432`

4. Update `.env`:
```env
DB_HOST=db.xxxxx.supabase.co
DB_PASSWORD=your_password
```

5. Run migrations:
```bash
python manage.py migrate
```

---

## Admin Features

### View Feedback
- Go to `/admin/feedback/`
- Pagination: 12 items per page
- Recent feedback shown first

### Filter Feedback
```
Search: By name, subject, message
Department: IT, CS, ECE, ME, CE, EE, Other
Rating: 1 to 5 stars
```

### Delete Feedback
- Click "Delete" on any feedback card
- Confirm deletion on next page
- Cannot be undone!

### Dashboard Stats
- Total feedback count
- Average rating
- Rating distribution (chart)
- Department breakdown
- Recent 5 feedbacks preview

---

## Common Commands

```bash
# Development
python manage.py runserver          # Run dev server
python manage.py runserver 0.0.0.0:8080  # Custom port

# Database
python manage.py migrate            # Run migrations
python manage.py makemigrations     # Create migrations
python manage.py dumpdata > data.json   # Backup data
python manage.py loaddata data.json      # Restore data

# Data Management
python manage.py createsuperuser    # Create admin
python manage.py shell              # Python shell
python manage.py test               # Run tests
python manage.py collectstatic      # Collect static files

# Utilities
python manage.py check              # Check for errors
python manage.py dbshell            # Connect to database
```

---

## Troubleshooting

### "No such table: feedback_app_feedback"
```bash
python manage.py migrate
```

### "Connection refused" (Database)
- Check `.env` Supabase credentials
- Verify network connectivity
- Check Supabase dashboard status

### "Admin login not working"
```bash
python manage.py createsuperuser
```

### "Static files not loading"
```bash
python manage.py collectstatic --noinput
```

### "Port 8000 already in use"
```bash
python manage.py runserver 0.0.0.0:8080
```

---

## Deployment Checklist

Before going live:

- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT = True`)
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Use environment variables for secrets
- [ ] Set up database backups
- [ ] Configure static file serving
- [ ] Set up error logging
- [ ] Test admin functionality
- [ ] Verify database optimization

---

## Project Structure At a Glance

```
project/
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
├── README.md                  # Overview
├── SETUP_GUIDE.md             # Detailed setup
├── API_DOCUMENTATION.md       # API reference
├── QUICK_REFERENCE.md         # This file
│
├── feedback_project/          # Project config
│   ├── settings.py            # Configuration
│   ├── urls.py                # Routing
│   ├── wsgi.py                # Production
│   └── asgi.py                # Async
│
├── feedback_app/              # Main app
│   ├── models.py              # Database models
│   ├── views.py               # Controllers
│   ├── forms.py               # Django forms
│   ├── urls.py                # App routes
│   ├── admin.py               # Admin config
│   ├── migrations/            # DB migrations
│   └── tests.py               # Unit tests
│
├── templates/                 # HTML pages
│   ├── base.html              # Base layout
│   ├── feedback_form.html      # Student form
│   ├── dashboard.html          # Admin dashboard
│   ├── login.html              # Admin login
│   ├── feedback_management.html # Feedback list
│   └── confirm_delete.html     # Delete confirm
│
├── static/                    # Static files
│   ├── css/style.css          # Styling
│   └── js/script.js            # Interactivity
│
└── .env                       # Environment (not tracked)
```

---

## Database Queries

### Get Total Feedback
```python
from feedback_app.models import Feedback
Feedback.objects.count()
```

### Get Average Rating
```python
from django.db.models import Avg
Feedback.objects.aggregate(Avg('rating'))
```

### Get 5-Star Feedback
```python
Feedback.objects.filter(rating=5)
```

### Get Feedback by Department
```python
Feedback.objects.filter(department='IT')
```

### Delete Old Feedback
```python
from django.utils import timezone
from datetime import timedelta

old_date = timezone.now() - timedelta(days=90)
Feedback.objects.filter(created_at__lt=old_date).delete()
```

---

## Performance Tips

1. **Enable Caching**: Cache dashboard stats
2. **Optimize Queries**: Use `select_related()`, `prefetch_related()`
3. **Index Database**: Add indexes on frequently queried fields
4. **Compress Assets**: GZIP compress CSS/JS
5. **CDN**: Serve static files from CDN in production
6. **Database Connection Pooling**: Use pgBouncer with Supabase

---

## Security Checklist

```
[✓] CSRF token in forms
[✓] SQL injection prevention (ORM)
[✓] XSS protection (template escaping)
[✓] Password hashing (Django auth)
[✓] Secure cookies
[✓] Admin login required
[✓] HTTPS in production
[✓] Environment variables for secrets
```

---

## Testing the Application

### Manual Testing Points

1. **Feedback Submission**
   - Fill form and submit
   - Check success message
   - Verify in admin panel

2. **Anonymous Submission**
   - Check anonymous option
   - Submit and verify in admin

3. **Admin Login**
   - Login with correct credentials
   - Verify dashboard loads
   - Check stats display

4. **Feedback Management**
   - Search by name
   - Filter by department
   - Filter by rating
   - Test pagination
   - Delete and confirm

5. **Responsive Design**
   - Test on mobile (375px width)
   - Test on tablet (768px width)
   - Test on desktop (1920px width)

---

## Useful Resources

- Django Docs: https://docs.djangoproject.com/
- Supabase Docs: https://supabase.com/docs
- Chart.js: https://www.chartjs.org/
- Font Awesome: https://fontawesome.com/

---

## Testing Commands

```bash
# Run all tests
python manage.py test

# Run app tests
python manage.py test feedback_app

# Run with verbosity
python manage.py test -v 2

# Run specific test
python manage.py test feedback_app.tests.FeedbackModelTest

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## Example Cron Jobs (Deployment)

### Backup Database Daily
```bash
0 2 * * * pg_dump "postgresql://user:pass@host/db" > backup_$(date +\%Y\%m\%d).sql
```

### Daily Newsletter
```bash
0 9 * * * python manage.py send_daily_feedback_report
```

### Cleanup Old Records
```bash
0 3 1 * * python manage.py delete_old_feedback --days=90
```

---

## Version Info

- **Django**: 4.2.7
- **Python**: 3.10+
- **PostgreSQL**: 13+
- **Node/npm**: Not required

---

**Last Updated**: February 2026
**Status**: Production Ready ✅
