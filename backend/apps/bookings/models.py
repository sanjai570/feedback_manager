from django.db import models
from apps.users.models import User
from apps.resources.models import Resource

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    bookingDate = models.DateField()
    timeSlot = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['resource', 'bookingDate', 'timeSlot'],
                name='unique_resource_booking'
            )
        ]

    def __str__(self):
        return f"{self.user.name} - {self.resource.name} - {self.bookingDate} {self.timeSlot}"
