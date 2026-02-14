# Feedback Collection System

A modern, production-ready feedback collection web application built with **Django** and **Supabase PostgreSQL**. Perfect for educational institutions to collect and manage student feedback.

## 🌟 Features

### Student Portal
- **Modern Feedback Form**: Clean, intuitive interface for submitting feedback
- **Rating System**: 1-5 star rating with interactive visualization
- **Anonymous Submission**: Option to submit feedback anonymously
- **Real-time Validation**: Instant feedback on form inputs
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Confirmation Messages**: Toast notifications for successful submissions

### Admin Dashboard
- **Secure Authentication**: Django built-in auth system with login protection
- **Dashboard Statistics**: 
  - Total feedback count
  - Average rating
  - Department-wise feedback distribution
  - Rating distribution chart
  - Recent feedback preview
- **Advanced Feedback Management**:
  - View all feedback in card format
  - Search feedback by student name, subject, or message
  - Filter by department and rating
  - Pagination for large datasets
  - Delete feedback with confirmation
- **Data Visualization**: Charts and graphs for quick insights

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Database**: Supabase PostgreSQL
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Authentication**: Django Auth System
- **Styling**: Modern CSS with gradient effects
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6.0.0

## 📋 Requirements

- Python 3.10+
- Virtual Environment (venv)
- Supabase Account
- Git

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd /Users/anu/Downloads/project
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Supabase

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:
```env
DB_HOST=db.xxxxx.supabase.co
DB_PASSWORD=your_password
DB_USER=postgres
DB_NAME=postgres
SECRET_KEY=your-secret-key
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your secure password)
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Visit:
- **Student Portal**: http://localhost:8000/
- **Admin Login**: http://localhost:8000/admin/login/
- **Django Admin**: http://localhost:8000/admin/

## 📁 Project Structure

```
project/
├── feedback_project/          # Django project settings
├── feedback_app/              # Main application
│   ├── models.py              # Feedback model
│   ├── views.py               # Views and logic
│   ├── forms.py               # Django forms
│   ├── urls.py                # URL routing
│   └── migrations/            # Database migrations
├── templates/                 # HTML templates
│   ├── base.html              # Base layout
│   ├── feedback_form.html      # Student form
│   ├── dashboard.html          # Admin dashboard
│   ├── login.html              # Admin login
│   ├── feedback_management.html# Feedback list
│   └── confirm_delete.html     # Delete confirmation
├── static/                    # Static files
│   ├── css/style.css          # Modern styling
│   └── js/script.js            # Interactivity
├── manage.py                  # Django CLI
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
└── SETUP_GUIDE.md             # Detailed setup instructions
```

## 🎨 UI/UX Highlights

- **Modern Design**: Clean, professional aesthetic with soft colors
- **Responsive Layout**: Mobile-first design that works on all devices
- **Interactive Elements**: Smooth animations and hover effects
- **Dashboard Cards**: Statistics displayed in attractive card format
- **Color-coded Ratings**: Visual feedback with color-gradient stars
- **Empty States**: Friendly messages when no data is available
- **Toast Notifications**: Non-intrusive success/error messages
- **Nice Table Design**: Well-organized feedback listing

## 🔐 Security Features

- ✅ CSRF Protection enabled
- ✅ SQL Injection prevention (Django ORM)
- ✅ User Authentication required for admin
- ✅ Password hashing with Django's auth
- ✅ XSS Protection
- ✅ Secure cookie settings
- ✅ Environment-based configuration

## 📊 Database Schema

### Feedback Model
```python
Feedback(
    student_name: CharField(100)
    department: CharField(choices)           # IT, CS, ECE, ME, CE, EE, Other
    year: CharField(choices)                 # 1st, 2nd, 3rd, 4th Year
    subject_or_faculty: CharField(200)
    rating: IntegerField(1-5)
    feedback_message: TextField
    is_anonymous: BooleanField
    created_at: DateTimeField(auto)
)
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with verbose output
python manage.py test -v 2

# Test specific app
python manage.py test feedback_app
```

## 🚢 Deployment

The project is ready for deployment on:
- Heroku
- PythonAnywhere
- AWS
- DigitalOcean
- Any server with Python + PostgreSQL

See `SETUP_GUIDE.md` for detailed deployment instructions.

## 📚 Admin Panel Features

The Django admin panel includes:
- Custom Feedback admin interface
- Filtering by department, rating, year, date
- Search by student name, subject, message
- Bulk actions
- Read-only created_at field
- Organized fieldsets

## 💡 Key Functionalities

### Student Side
1. Fill feedback form with validation
2. Rate using interactive star system
3. Option to stay anonymous
4. Submit with confirmation
5. Clear form anytime

### Admin Side
1. Login securely
2. View dashboard with stats
3. See recent feedback
4. Browse all feedback with pagination
5. Filter and search feedback
6. Delete unwanted feedback
7. View rating distribution
8. Check department statistics

## 🎯 Perfect For

- **Colleges & Universities**: Collect student feedback on courses
- **Departments**: Gather feedback on faculty and courses
- **Institutions**: Annual feedback collection
- **Research Projects**: Real-world Django application example
- **Portfolio Projects**: Showcase professional web development

## 📝 License

MIT License - Feel free to use and modify

## 📞 Support

For setup help, check `SETUP_GUIDE.md` or review Django documentation at:
https://docs.djangoproject.com/

---

**Built with ❤️ using Django and Supabase**

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: February 2026
