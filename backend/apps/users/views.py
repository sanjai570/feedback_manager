from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsAdmin, IsStaffOrAdmin, IsOwnerOrAdmin
from .services import UserService
from .serializers import UserSerializer

# Add UserMeView import or definition check


class UserListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [] # Allow signup
        return [IsAuthenticated(), IsStaffOrAdmin()] # Only Staff/Admin see list
    def get(self, request):
        status_param = request.query_params.get('status')
        users = UserService.get_all_users(status=status_param)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            # Security: Only ADMIN can set specific roles (like STAFF).
            # Public signup (Anonymous) or non-Admins cannot set role.
            if request.user.is_authenticated and request.user.role == 'ADMIN':
                if 'role' in request.data:
                    validated_data['role'] = request.data['role']
            
            # Service will verify ADMIN_EMAILS enforcement and default to STUDENT if role is missing
            user = UserService.create_user(validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        print(f"DEBUG: User Creation Failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Admin/Staff can view any user? 
        # Requirement: "STUDENT: Can only view and update OWN profile".
        # So Admin/Staff should be able to view others.
        from apps.common.permissions import IsOwner, IsStaffOrAdmin
        
        # Check if user has permission
        # APIView check_object_permissions doesn't work well without a queryset or get_object.
        # We'll implement manual check or use permission classes on the view.
        # But for get/put/delete, the logic differs.
        # Ideally, we use `self.check_object_permissions`.
        
        user = UserService.get_user_by_id(pk)
        
        # We need a custom logic here or rely on IsOwnerOrStaffOrAdmin?
        # Let's enforce manually for clarity as requested "Strict Backend Enforcement".
        
        is_owner = request.user.id == user.id
        is_staff_or_admin = request.user.role in ['ADMIN', 'STAFF']
        
        if not (is_owner or is_staff_or_admin):
             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        user = UserService.get_user_by_id(pk)
        
        # STUDENT: Update OWN profile.
        # ADMIN: Update anyone.
        # STAFF: ? Requirement says "Read-only" for Users module for STAFF.
        # "STAFF: Read-only". So Staff CANNOT update users.
        
        if request.user.role == 'STAFF':
            return Response({'error': 'Permission denied: Staff are read-only'}, status=status.HTTP_403_FORBIDDEN)
            
        is_owner = request.user.id == user.id
        is_admin = request.user.role == 'ADMIN'
        
        if not (is_owner or is_admin):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Prevent role update by non-admin
        if 'role' in request.data and request.user.role != 'ADMIN':
             return Response({'error': 'Permission denied: Cannot change role'}, status=status.HTTP_403_FORBIDDEN)
             
        serializer = UserSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            updated_user = UserService.update_user(pk, serializer.validated_data)
            return Response(UserSerializer(updated_user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # "STAFF cannot delete users".
        # "STUDENT ... Block editing others". implied student cannot delete.
        # "ADMIN: Full CRUD".
        # So only Admin can delete.
        if request.user.role != 'ADMIN':
             return Response({'error': 'Permission denied: Only Admin can delete users'}, status=status.HTTP_403_FORBIDDEN)
             
        UserService.delete_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserLoginView(APIView):
    permission_classes = [] # Allow anonymous

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from .models import User
            from django.contrib.auth.hashers import check_password
            from rest_framework_simplejwt.tokens import RefreshToken
            
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                 refresh = RefreshToken.for_user(user)
                 return Response({
                     'refresh': str(refresh),
                     'access': str(refresh.access_token),
                     # Optional: return user data too if needed by frontend immediately
                     'id': user.id,
                     'name': user.name,
                     'email': user.email,
                     'role': user.role
                 })
            else:
                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': f'Internal Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetRequestView(APIView):
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from .models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construct Link (assuming frontend runs on 5173)
            reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"
            
            # Send Email
            print(f"--- DETECTED PASSWORD RESET REQUEST ---")
            print(f"To: {email}")
            print(f"Reset Link: {reset_link}")
            print(f"---------------------------------------")
            
            # We also use send_mail to trigger the console backend
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            return Response({'message': 'Password reset link sent to email (check console)'})
            
        except User.DoesNotExist:
            # For security, we might want to return success even if user not found, 
            # but for this internal tool, 404 is fine or generic message.
            # Let's return generic success to avoid enumeration, 
            # OR specific for this dev phase? User asked "what about...", let's be helpful.
            return Response({'error': 'User with this email not found'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    permission_classes = []

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        if not password:
             return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from .models import User
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str
        from django.contrib.auth.hashers import make_password
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.password = make_password(password)
                user.save()
                return Response({'message': 'Password has been reset successfully'})
            else:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
