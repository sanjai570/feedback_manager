#!/usr/bin/env python
"""Test password reset functionality"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.contrib.auth.models import User
from feedback_app.forms import StudentPasswordResetForm

# Test password reset form with existing user
print("✅ Testing Password Reset Form\n")

# Get an existing user
users = User.objects.exclude(username='admin')[:1]

if users:
    user = users[0]
    print(f"Testing with user: {user.username} ({user.email})")
    
    # Test valid email
    form = StudentPasswordResetForm({'email': user.email})
    if form.is_valid():
        print(f"✅ Form validation passed for email: {user.email}")
    else:
        print(f"❌ Form validation failed: {form.errors}")
    
    # Test invalid email
    form = StudentPasswordResetForm({'email': 'nonexistent@example.com'})
    if not form.is_valid():
        print(f"✅ Form correctly rejected non-existent email")
        print(f"   Error: {form.errors['email'][0]}")
    else:
        print(f"❌ Form should reject non-existent email")
    
    print("\n✅ Password Reset Feature Ready!")
    print("   URLs:")
    print("   • Forgot Password: http://localhost:8000/password-reset/")
    print("   • Reset Link (in email): http://localhost:8000/password-reset/<token>/")
    print("   • Done Page: http://localhost:8000/password-reset/done/")
    print("   • Complete: http://localhost:8000/password-reset/complete/")
    
else:
    print("No test users found. Create some first!")
