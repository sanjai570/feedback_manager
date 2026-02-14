# Feedback Collection System - API Documentation

## Overview

This document outlines the API endpoints and data structures for the Feedback Collection System.

## Base URL

```
http://localhost:8000
```

## API Endpoints

### 1. Student Feedback Submission

#### Endpoint
```
POST /
```

#### Description
Submit a new feedback entry

#### Request Form Data
```
student_name: string (required, max 100 chars)
department: string (required, choices: IT, CS, ECE, ME, CE, EE, OTHER)
year: string (required, choices: 1, 2, 3, 4)
subject_or_faculty: string (required, max 200 chars)
rating: integer (required, 1-5)
feedback_message: string (required, min 10 chars)
is_anonymous: boolean (optional, default: false)
```

#### Response
- **Success**: Redirects to feedback form with success message
- **Error**: Returns form with validation errors

#### Example
```bash
curl -X POST http://localhost:8000/ \
  -F "student_name=John Doe" \
  -F "department=IT" \
  -F "year=3" \
  -F "subject_or_faculty=Database Systems" \
  -F "rating=5" \
  -F "feedback_message=Excellent course with great teaching methodology" \
  -F "is_anonymous=false"
```

---

### 2. Admin Login

#### Endpoint
```
POST /admin/login/
```

#### Description
Authenticate admin user

#### Request Form Data
```
username: string (required)
password: string (required)
```

#### Response
- **Success**: Redirects to dashboard
- **Error**: Returns login form with error message

#### Example
```bash
curl -X POST http://localhost:8000/admin/login/ \
  -d "username=admin" \
  -d "password=yourpassword"
```

---

### 3. Admin Logout

#### Endpoint
```
GET /admin/logout/
```

#### Description
Logout admin user

#### Response
- Redirects to feedback form

#### Example
```bash
curl http://localhost:8000/admin/logout/
```

---

### 4. Admin Dashboard

#### Endpoint
```
GET /admin/dashboard/
```

#### Description
View admin dashboard with statistics

#### Authentication
- Required: Admin user (staff or superuser)

#### Response
Returns HTML page with:
- Total feedback count
- Average rating
- Rating distribution chart
- Department-wise feedback count
- Recent feedback preview

#### Example
```bash
curl -b cookies.txt http://localhost:8000/admin/dashboard/
```

---

### 5. Feedback Management

#### Endpoint
```
GET /admin/feedback/
```

#### Description
View and manage all feedback with filtering

#### Authentication
- Required: Admin user

#### Query Parameters
```
department: string (optional) - Filter by department
rating: integer (optional) - Filter by rating (1-5)
search: string (optional) - Search in name, subject, message
page: integer (optional) - Page number (default: 1)
```

#### Response
Returns HTML page with feedback list and pagination

#### Examples
```bash
# View all feedback
curl -b cookies.txt http://localhost:8000/admin/feedback/

# Filter by department
curl -b cookies.txt "http://localhost:8000/admin/feedback/?department=IT"

# Filter by rating
curl -b cookies.txt "http://localhost:8000/admin/feedback/?rating=5"

# Search feedback
curl -b cookies.txt "http://localhost:8000/admin/feedback/?search=john"

# Combined filters with pagination
curl -b cookies.txt "http://localhost:8000/admin/feedback/?department=IT&rating=5&search=john&page=2"
```

---

### 6. Delete Feedback

#### Endpoint
```
GET /admin/feedback/<id>/delete/
POST /admin/feedback/<id>/delete/
```

#### Description
View deletion confirmation or delete feedback

#### Authentication
- Required: Admin user

#### Path Parameters
```
id: integer - Feedback ID
```

#### Response
- **GET**: Returns confirmation page
- **POST**: Deletes feedback and redirects

#### Example
```bash
# View confirmation
curl -b cookies.txt http://localhost:8000/admin/feedback/1/delete/

# Delete feedback
curl -X POST -b cookies.txt http://localhost:8000/admin/feedback/1/delete/
```

---

### 7. Feedback Statistics API

#### Endpoint
```
GET /api/stats/
```

#### Description
Get feedback statistics in JSON format (for AJAX)

#### Authentication
- Required: Admin user

#### Response
```json
{
    "total": 45,
    "average_rating": 4.2,
    "rating_distribution": [
        {"rating": 1, "count": 2},
        {"rating": 2, "count": 3},
        {"rating": 3, "count": 8},
        {"rating": 4, "count": 18},
        {"rating": 5, "count": 14}
    ]
}
```

#### Example
```bash
curl -b cookies.txt http://localhost:8000/api/stats/
```

---

## Data Models

### Feedback Model

```javascript
{
    "id": 1,
    "student_name": "John Doe",
    "department": "IT",
    "year": "3",
    "subject_or_faculty": "Database Systems",
    "rating": 5,
    "feedback_message": "Excellent course with great teaching methodology",
    "is_anonymous": false,
    "created_at": "2024-02-14T10:30:00Z"
}
```

### User Model

```javascript
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true,
    "is_superuser": true,
    "is_active": true,
    "date_joined": "2024-02-14T00:00:00Z"
}
```

---

## Error Handling

### Validation Errors

```
Field errors are returned in the form response with error messages.
```

### Authentication Errors

```
401 Unauthorized - User not authenticated
403 Forbidden - User lacks required permissions
```

### Not Found

```
404 Not Found - Resource does not exist
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 302 | Found (Redirect) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Authentication

The application uses Django's built-in session-based authentication.

### Login Flow
1. Submit credentials to `/admin/login/`
2. Django creates a session cookie
3. Use the session cookie for subsequent requests

### Logout Flow
1. Access `/admin/logout/`
2. Django invalidates the session
3. Redirect to feedback form

---

## Pagination

The feedback management endpoint returns paginated results.

```
Default: 12 items per page
URL parameter: ?page=2
```

Example response includes:
- Current page number
- Total number of pages
- Links to previous/next pages

---

## CSRF Protection

All POST requests require CSRF token:

```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

Or in AJAX:
```javascript
fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: formData
});
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider adding:

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h', method='POST')
def feedback_form(request):
    # ...
```

---

## CORS

CORS is not enabled by default. To enable for external APIs:

```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://example.com",
]
```

---

## Testing Endpoints

### Using curl

```bash
# Login
curl -c cookies.txt -X POST http://localhost:8000/admin/login/ \
  -d "username=admin&password=password"

# Get dashboard
curl -b cookies.txt http://localhost:8000/admin/dashboard/

# Logout
curl -b cookies.txt http://localhost:8000/admin/logout/
```

### Using JavaScript

```javascript
// Login
fetch('/admin/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'username=admin&password=password'
});

// Get stats
fetch('/api/stats/')
    .then(r => r.json())
    .then(data => console.log(data));
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2024 | Initial release |

---

For more information, see `README.md` and `SETUP_GUIDE.md`.
