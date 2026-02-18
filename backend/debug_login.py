
import os
import django
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from apps.users.views import UserLoginView

def debug_login():
    factory = APIRequestFactory()
    view = UserLoginView.as_view()

    print("\n--- Testing Login with New User ---")
    from apps.users.services import UserService
    try:
        UserService.create_user({'name': 'Debug Student', 'email': 'debug_student@test.com', 'password': 'password123', 'role': 'STUDENT'})
    except Exception:
        pass # Already exists

    request = factory.post('/api/users/login/', {'email': 'debug_student@test.com', 'password': 'password123'}, format='json')
    try:
        response = view(request)
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_login()
