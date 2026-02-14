from django.contrib import admin
from .models import Event, StudentProfile, Feedback, EventAttendance


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'venue', 'organizer', 'get_feedback_count', 'get_average_rating')
    list_filter = ('event_date', 'created_at')
    search_fields = ('title', 'description', 'venue', 'organizer')
    ordering = ('-event_date',)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'description', 'event_date', 'venue', 'organizer', 'image', 'created_at', 'updated_at')

    def get_feedback_count(self, obj):
        return obj.get_feedback_count()
    get_feedback_count.short_description = 'Feedback Count'

    def get_average_rating(self, obj):
        rating = obj.get_average_rating()
        return f"⭐ {rating:.1f}" if rating else "No rating"
    get_average_rating.short_description = 'Average Rating'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user_email', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Student Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'event', 'rating', 'created_at')
    list_filter = ('event', 'rating', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'feedback_message', 'event__title')
    ordering = ('-created_at',)
    readonly_fields = ('student', 'event', 'created_at', 'updated_at')
    fields = ('student', 'event', 'rating', 'feedback_message', 'created_at', 'updated_at')

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    get_student_name.short_description = 'Student'


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'event', 'attendance_date')
    list_filter = ('event', 'attendance_date')
    search_fields = ('student__first_name', 'student__last_name', 'event__title')
    ordering = ('-attendance_date',)
    readonly_fields = ('attendance_date',)

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
    get_student_name.short_description = 'Student'
