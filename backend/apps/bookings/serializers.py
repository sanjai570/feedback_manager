from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        source='user'
    )
    resourceId = serializers.PrimaryKeyRelatedField(
        queryset=Booking.resource.field.related_model.objects.all(), 
        source='resource'
    )

    class Meta:
        model = Booking
        fields = ['id', 'userId', 'resourceId', 'bookingDate', 'timeSlot', 'status']
