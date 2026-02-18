from .models import Booking
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class BookingService:
    @staticmethod
    @staticmethod
    def create_booking(data):
        from django.db import transaction
        from apps.resources.models import Resource
        
        resource_id = data.get('resource').id if hasattr(data.get('resource'), 'id') else data.get('resource')
        date = data.get('bookingDate')
        time = data.get('timeSlot')

        # Use atomic transaction to ensure data integrity
        with transaction.atomic():
            # Lock the resource row to prevent concurrent booking attempts for the same resource
            # This serializes checks for this specific resource
            _ = Resource.objects.select_for_update().get(id=resource_id)
            
            # Double Check conflict inside the lock
            if Booking.objects.filter(resource_id=resource_id, bookingDate=date, timeSlot=time).exists():
                raise ValidationError("Resource is already booked for this date and time slot.")

            # Enforce PENDING status on creation
            data['status'] = 'PENDING'
            booking = Booking.objects.create(**data)
            return booking

    @staticmethod
    def get_all_bookings():
        return Booking.objects.all()

    @staticmethod
    def update_booking_status(booking_id, status):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = status
        booking.save()
        return booking

    @staticmethod
    def delete_booking(booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return True
