"""
Django settings for asgi configuration of feedback_project.
Useful for running production server with gunicorn or uvicorn.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

OS_ENVIRON = os.environ.copy()
os_getenv = os.getenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')

import django
django.setup()

application = None
