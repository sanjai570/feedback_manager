from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json

from .models import Event, Feedback, StudentProfile, EventAttendance
from .forms import (
    StudentRegistrationForm, StudentAuthenticationForm, AdminAuthenticationForm,
    EventForm, EventFeedbackForm, EventFilterForm, StudentPasswordResetForm, StudentSetPasswordForm
)


# ============================================================================
# STUDENT AUTHENTICATION VIEWS
# ============================================================================

def student_register(request):
    """Student Registration View"""
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'✅ Welcome {user.first_name}! Your account has been created.')
            return redirect('student_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Student Registration',
    }
    return render(request, 'student_register.html', context)


def student_login(request):
    """Student Login View"""
    if request.user.is_authenticated:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = StudentAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StudentAuthenticationForm()

    context = {
        'form': form,
        'page_title': 'Student Login',
    }
    return render(request, 'student_login.html', context)


def student_logout(request):
    """Student Logout View"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ============================================================================
# STUDENT VIEWS
# ============================================================================

@login_required(login_url='student_login')
def student_dashboard(request):
    """Student Dashboard - View all events"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        return redirect('student_login')

    # Get all events, ordered by date
    events = Event.objects.all().order_by('-event_date')

    # Check which events student has already given feedback for
    feedback_events = Feedback.objects.filter(student=request.user).values_list('event_id', flat=True)

    # Add feedback status to events
    for event in events:
        event.has_feedback = event.id in feedback_events

    # Pagination
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'student_profile': student_profile,
        'page_title': 'Events Dashboard',
    }
    return render(request, 'student_dashboard.html', context)


@login_required(login_url='student_login')
def event_detail(request, event_id):
    """Event Detail - View event and submit feedback"""
    event = get_object_or_404(Event, id=event_id)
    student_profile = request.user.student_profile

    # Check if student has already submitted feedback
    existing_feedback = Feedback.objects.filter(student=request.user, event=event).first()

    if request.method == 'POST' and not existing_feedback:
        form = EventFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.event = event
            feedback.save()

            # Mark attendance if not already marked
            EventAttendance.objects.get_or_create(student=request.user, event=event)

            messages.success(request, '✅ Thank you! Your feedback has been submitted.')
            return redirect('student_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        if existing_feedback:
            messages.info(request, 'You have already submitted feedback for this event.')
        form = EventFeedbackForm() if not existing_feedback else None

    context = {
        'event': event,
        'student_profile': student_profile,
        'form': form,
        'existing_feedback': existing_feedback,
        'page_title': event.title,
    }
    return render(request, 'event_detail.html', context)


# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================

def admin_login(request):
    """Admin Login View"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access.')
    else:
        form = AdminAuthenticationForm()

    context = {
        'form': form,
        'page_title': 'Admin Login',
    }
    return render(request, 'admin_login.html', context)


def admin_logout(request):
    """Admin Logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ============================================================================
# ADMIN VIEWS
# ============================================================================

@login_required(login_url='admin_login')
def admin_dashboard(request):
    """Admin Dashboard with Statistics"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Statistics
    total_events = Event.objects.count()
    total_feedback = Feedback.objects.count()
    average_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    # Event-wise feedback count
    event_stats = Event.objects.annotate(
        feedback_count=Count('feedback'),
        avg_rating=Avg('feedback__rating')
    ).order_by('-feedback_count')

    # Recent feedback
    recent_feedback = Feedback.objects.select_related('event', 'student').order_by('-created_at')[:5]

    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = Feedback.objects.filter(rating=i).count()

    context = {
        'total_events': total_events,
        'total_feedback': total_feedback,
        'average_rating': round(average_rating, 1),
        'event_stats': event_stats,
        'recent_feedback': recent_feedback,
        'rating_distribution': json.dumps(rating_distribution),
        'page_title': 'Admin Dashboard',
    }
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='admin_login')
def event_management(request):
    """Admin - List and manage events"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    events = Event.objects.all().order_by('-event_date')

    # Pagination
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add feedback count to events
    for event in page_obj:
        event.feedback_count = Feedback.objects.filter(event=event).count()
        event.avg_rating = Feedback.objects.filter(event=event).aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        'page_obj': page_obj,
        'page_title': 'Event Management',
    }
    return render(request, 'event_management.html', context)


@login_required(login_url='admin_login')
def event_create(request):
    """Admin - Create new event"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'✅ Event "{event.title}" created successfully!')
            return redirect('event_management')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EventForm()

    context = {
        'form': form,
        'page_title': 'Create Event',
    }
    return render(request, 'event_form.html', context)


@login_required(login_url='admin_login')
def event_edit(request, event_id):
    """Admin - Edit event"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'✅ Event "{event.title}" updated successfully!')
            return redirect('event_management')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'page_title': f'Edit Event - {event.title}',
    }
    return render(request, 'event_form.html', context)


@login_required(login_url='admin_login')
def event_delete(request, event_id):
    """Admin - Delete event"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'✅ Event "{event_title}" deleted successfully!')
        return redirect('event_management')

    context = {
        'event': event,
        'page_title': 'Delete Event',
    }
    return render(request, 'event_confirm_delete.html', context)


@login_required(login_url='admin_login')
def event_feedback(request, event_id):
    """Admin - View feedback for specific event"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    event = get_object_or_404(Event, id=event_id)
    feedbacks = Feedback.objects.filter(event=event).select_related('student').order_by('-created_at')

    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        feedbacks = feedbacks.filter(rating=int(rating))

    # Search
    search = request.GET.get('search')
    if search:
        feedbacks = feedbacks.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(feedback_message__icontains=search)
        )

    # Statistics for event
    average_rating = feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0
    total_feedback_count = feedbacks.count()

    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = Feedback.objects.filter(event=event, rating=i).count()

    # Pagination
    paginator = Paginator(feedbacks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'event': event,
        'page_obj': page_obj,
        'average_rating': round(average_rating, 1),
        'total_feedback': total_feedback_count,
        'rating_distribution': json.dumps(rating_distribution),
        'page_title': f'{event.title} - Feedback Analytics',
    }
    return render(request, 'event_feedback_analytics.html', context)


@login_required(login_url='admin_login')
def delete_feedback(request, feedback_id):
    """Admin - Delete feedback"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')

    feedback = get_object_or_404(Feedback, id=feedback_id)
    event = feedback.event

    if request.method == 'POST':
        feedback.delete()
        messages.success(request, '✅ Feedback deleted successfully!')
        return redirect('event_feedback', event_id=event.id)

    context = {
        'feedback': feedback,
        'page_title': 'Delete Feedback',
    }
    return render(request, 'feedback_confirm_delete.html', context)


# ============================================================================
# PUBLIC VIEWS
# ============================================================================

def home(request):
    """Home Page"""
    upcoming_events = Event.objects.filter(event_date__gte=datetime.now()).count()
    total_feedback = Feedback.objects.count()

    context = {
        'upcoming_events': upcoming_events,
        'total_feedback': total_feedback,
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@login_required(login_url='admin_login')
def api_dashboard_stats(request):
    """API - Dashboard statistics"""
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    stats = {
        'total_events': Event.objects.count(),
        'total_feedback': Feedback.objects.count(),
        'average_rating': float(Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0),
        'recent_feedbacks': list(
            Feedback.objects.select_related('student', 'event')
            .order_by('-created_at')[:5]
            .values('student__first_name', 'student__last_name', 'event__title', 'rating')
        )
    }
    return JsonResponse(stats)


# ==================== PASSWORD RESET VIEWS ====================

class StudentPasswordResetView(PasswordResetView):
    """Password reset view for students"""
    form_class = StudentPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/password-reset/done/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Password reset link has been sent to your email.')
        return super().form_valid(form)


class StudentPasswordResetDoneView(PasswordResetDoneView):
    """Password reset done view"""
    template_name = 'password_reset_done.html'


class StudentPasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset confirm view"""
    form_class = StudentSetPasswordForm
    template_name = 'password_reset_confirm.html'
    success_url = '/password-reset/complete/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfully reset. You can now login.')
        return super().form_valid(form)


class StudentPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete view"""
    template_name = 'password_reset_complete.html'

