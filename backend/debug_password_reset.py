
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from apps.users.views import PasswordResetRequestView

def debug_reset():
    factory = APIRequestFactory()
    view = PasswordResetRequestView.as_view()

    # Test Case 1: Existing Admin
    print("\n--- Testing Admin Reset ---")
    request = factory.post('/api/users/reset-password/', {'email': 'admin1@college.edu'}, format='json')
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")

    # Test Case 2: Validation Error?
    print("\n--- Testing Invalid Email ---")
    request = factory.post('/api/users/reset-password/', {'email': ''}, format='json')
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")

if __name__ == "__main__":
    try:
        debug_reset()
    except Exception as e:
        print(f"CRASH: {e}")
