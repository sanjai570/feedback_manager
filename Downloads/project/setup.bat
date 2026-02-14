@echo off
REM Feedback Collection System - Windows Setup Script

color 0B
echo ========================================
echo  Feedback Collection System - Setup
echo ========================================
echo.

REM Check Python version
echo [1/7] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo X Python is not installed
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo [2/7] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo [4/7] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo [OK] Dependencies installed
echo.

REM Check for .env file
echo [5/7] Setting up environment variables...
if not exist ".env" (
    copy .env.example .env
    echo [WARNING] .env file created from template
    echo [WARNING] Please edit .env with your Supabase credentials
    echo Please configure the .env file and press any key...
    pause >nul
)
echo [OK] Environment configured
echo.

REM Run migrations
echo [6/7] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    color 0C
    echo X Migration failed. Check your database connection.
    pause
    exit /b 1
)
echo [OK] Migrations completed
echo.

REM Create superuser
echo [7/7] Creating admin account...
echo You will be prompted to create a superuser account
python manage.py createsuperuser

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start the development server:
echo    python manage.py runserver
echo.
echo 2. Access the application:
echo    Student Portal: http://localhost:8000/
echo    Admin Login:    http://localhost:8000/admin/login/
echo.
echo 3. For detailed setup guide:
echo    type SETUP_GUIDE.md
echo.
pause
