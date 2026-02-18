from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        print(f"DEBUG: Authenticating token: {validated_token}")
        try:
            from apps.users.models import User
            user_id = validated_token['user_id']
            print(f"DEBUG: User ID from token: {user_id}")
            user = User.objects.get(id=user_id)
            print(f"DEBUG: User found: {user}")
            return user
        except ImportError:
             print("DEBUG: Import Error")
             raise AuthenticationFailed('User model import failed', code='import_error')
        except User.DoesNotExist:
            print("DEBUG: User DoesNotExist")
            raise AuthenticationFailed('User not found', code='user_not_found')
        except KeyError:
             print("DEBUG: KeyError in token")
             raise AuthenticationFailed('Token contained no recognizable user identification', code='token_not_valid')
        except Exception as e:
            print(f"DEBUG: Unexpected error: {e}")
            raise AuthenticationFailed(f'Authentication error: {e}', code='auth_error')
