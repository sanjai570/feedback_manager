from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'resource', 'bookingDate', 'timeSlot', 'status')
    list_filter = ('status', 'bookingDate')
    search_fields = ('user__name', 'resource__name')
