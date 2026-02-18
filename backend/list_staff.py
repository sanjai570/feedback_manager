
import os
import django
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def list_staff():
    staff_users = User.objects.filter(role='STAFF')
    if not staff_users.exists():
        print("No Staff users found.")
    else:
        print("\n--- Staff Users ---")
        for user in staff_users:
            print(f"Name: {user.name}, Email: {user.email}")
        print("-------------------")

if __name__ == "__main__":
    list_staff()
