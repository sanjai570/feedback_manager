from .models import User
from django.shortcuts import get_object_or_404

class UserService:
    @staticmethod
    @staticmethod
    @staticmethod
    def create_user(data):
        from django.contrib.auth.hashers import make_password
        from config.constants import ADMIN_EMAILS

        # Security: Enforce Role Rules
        email = data.get('email')
        
        if email in ADMIN_EMAILS:
            data['role'] = 'ADMIN'
        elif 'role' not in data:
            # Force STUDENT for public signups (where role is stripped/missing)
            data['role'] = 'STUDENT'
        # If 'role' is already in data (injected by View for Admin), we respect it.
        
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        # Remove any unexpected fields just in case? No, serializer handles limits.
        
        user = User.objects.create(**data)
        return user

    @staticmethod
    def get_all_users(status=None):
        users = User.objects.all()
        if status:
            users = users.filter(status=status)
        return users

    @staticmethod
    def get_user_by_id(user_id):
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def update_user(user_id, data):
        user = get_object_or_404(User, id=user_id)
        from django.contrib.auth.hashers import make_password
        for key, value in data.items():
            if key == 'password':
                value = make_password(value)
            setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return True
