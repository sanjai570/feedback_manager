from django.urls import path
from . import views

urlpatterns = [
    # PUBLIC VIEWS
    path('', views.home, name='home'),

    # STUDENT AUTHENTICATION
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    
    # PASSWORD RESET
    path('password-reset/', views.StudentPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.StudentPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.StudentPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.StudentPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # STUDENT VIEWS
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/event/<int:event_id>/', views.event_detail, name='event_detail'),

    # ADMIN AUTHENTICATION
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),

    # ADMIN VIEWS
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/events/', views.event_management, name='event_management'),
    path('admin/events/create/', views.event_create, name='event_create'),
    path('admin/events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('admin/events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('admin/events/<int:event_id>/feedback/', views.event_feedback, name='event_feedback'),
    path('admin/feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),

    # API ENDPOINTS
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]
