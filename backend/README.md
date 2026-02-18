# Campus Resource Management System Backend

A comprehensive backend for managing campus resources, users, and bookings.

## Tech Stack
- **Languages**: Python
- **Framework**: Django, Django REST Framework (DRF)
- **Database**: SQLite (default) / Configurable

## Project Structure
```
backend/
├── manage.py
├── config/           # Project configuration
├── apps/
│   ├── users/        # User management
│   ├── resources/    # Resource management
│   └── bookings/     # Booking logic
```

## Setup & Installation

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Users
- `GET /api/users/` - List all users (filter `?status=ACTIVE`)
- `POST /api/users/` - Create a user
- `GET /api/users/<id>/` - Get user details
- `PUT /api/users/<id>/` - Update user
- `DELETE /api/users/<id>/` - Delete user

### Resources
- `GET /api/resources/` - List all resources
- `POST /api/resources/` - Create a resource
- `PUT /api/resources/<id>/` - Update resource
- `DELETE /api/resources/<id>/` - Delete resource

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create booking (Checks for conflicts)
- `PUT /api/bookings/<id>/` - Update booking status
- `DELETE /api/bookings/<id>/` - Delete booking

## Frontend (React)

The project includes a React frontend in the `frontend/` directory.

### Quick Start
1.  Navigate to `frontend/`: `cd frontend`
2.  Install dependencies: `npm install`
3.  Run development server: `npm run dev`
4.  Access at `http://localhost:5173`

The frontend is configured to proxy API requests to `http://127.0.0.1:8000`. Ensure the Django backend is running.

## Running the Whole Project

To start both the backend and frontend simultaneously, use the provided script:

```bash
./start_project.sh
```

This will launch:
1.  Django Backend on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
2.  React Frontend on [http://localhost:5173/](http://localhost:5173/)

## Business Rules
- **Double Booking**: A resource cannot be booked for the same date and time slot.
- **Service Layer**: All business logic resides in `services.py`.
