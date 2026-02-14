#!/usr/bin/env python
"""Test new departments"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from feedback_app.models import StudentProfile

print("✅ Available Departments:")
for dept_code, dept_name in StudentProfile.DEPARTMENT_CHOICES:
    print(f"   • {dept_code}: {dept_name}")
