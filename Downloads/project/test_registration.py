#!/usr/bin/env python
"""Test registration functionality"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.contrib.auth.models import User
from feedback_app.models import StudentProfile
from feedback_app.forms import StudentRegistrationForm

# Clean up test user if exists
User.objects.filter(username='testuser123').delete()

# Test full registration
data = {
    'first_name': 'Alex',
    'last_name': 'Test',
    'email': 'alex.test@college.edu',
    'username': 'testuser123',
    'password1': 'MyStrongPassword@2026',
    'password2': 'MyStrongPassword@2026',
    'department': 'IT',
    'year': '2'
}

form = StudentRegistrationForm(data)
if form.is_valid():
    user = form.save()
    profile = StudentProfile.objects.get(user=user)
    print("✅ REGISTRATION SUCCESSFUL!")
    print(f"   User: {user.username}")
    print(f"   Name: {user.first_name} {user.last_name}")
    print(f"   Email: {user.email}")
    print(f"   Department: {profile.get_department_display()}")
    print(f"   Year: {profile.get_year_display()}")
    print("\n✓ You can now login with:")
    print(f"  Username: testuser123")
    print(f"  Password: MyStrongPassword@2026")
else:
    print("❌ Registration failed:")
    for field, errors in form.errors.items():
        for error in errors:
            print(f"  {field}: {error}")
