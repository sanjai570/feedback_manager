from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Event(models.Model):
    """College Event Model"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    organizer = models.CharField(max_length=100)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"

    def get_average_rating(self):
        """Get average rating for this event"""
        feedbacks = self.feedback_set.all()
        if feedbacks.exists():
            return round(sum([f.rating for f in feedbacks]) / feedbacks.count(), 1)
        return 0

    def get_feedback_count(self):
        """Get total feedback count"""
        return self.feedback_set.count()


class StudentProfile(models.Model):
    """Extended Student Profile"""
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('ECE', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        ('AIML', 'Artificial Intelligence & Machine Learning'),
        ('AIDS', 'Artificial Intelligence & Data Science'),
        ('OTHER', 'Other'),
    ]

    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_department_display()}"


class Feedback(models.Model):
    """Event-based Feedback Model"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    feedback_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('student', 'event')  # One feedback per student per event
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.event.title} ({self.rating}★)"


class EventAttendance(models.Model):
    """Track which students attended which events"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    attendance_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
