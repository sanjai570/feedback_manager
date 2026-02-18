
import os
import django
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from apps.users.views import UserListCreateView
import json

def debug_signup():
    factory = APIRequestFactory()
    view = UserListCreateView.as_view()

    print("\n--- Testing Signup ---")
    data = {
        'name': 'Test Signup User',
        'email': 'test_signup@example.com',
        'password': 'password123',
        'phone': '1234567890'
    }
    request = factory.post('/api/users/', data, format='json')
    
    try:
        response = view(request)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_signup()
