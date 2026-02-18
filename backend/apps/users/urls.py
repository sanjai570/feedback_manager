from django.urls import path, include
from .views import UserListCreateView, UserDetailView, UserLoginView, UserMeView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
