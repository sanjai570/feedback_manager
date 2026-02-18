from django.db import models

class Resource(models.Model):
    TYPE_CHOICES = (
        ('LAB', 'Lab'),
        ('CLASSROOM', 'Classroom'),
        ('EVENT_HALL', 'Event Hall'),
    )
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.name} ({self.type})"
