
import os
import django
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.forms import UserCreationForm, UserChangeForm
from apps.users.admin import UserAdmin
from apps.users.models import User
from django.contrib.admin.sites import AdminSite

def verify_admin():
    print("--- Verifying Admin Forms ---")
    try:
        # Test Creation Form
        form = UserCreationForm()
        print("UserCreationForm instantiated successfully.")
        
        # Test Change Form
        user = User.objects.first()
        if user:
            form = UserChangeForm(instance=user)
            print("UserChangeForm instantiated successfully.")
        
        # Test Admin Registration
        site = AdminSite()
        admin_instance = UserAdmin(User, site)
        print("UserAdmin instantiated successfully.")
        
        # Check fieldsets
        print(f"Add Fieldsets: {admin_instance.add_fieldsets}")
        print(f"Fieldsets: {admin_instance.fieldsets}")
        
        print("SUCCESS: Admin config looks valid.")
        
    except Exception as e:
        print(f"FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_admin()
