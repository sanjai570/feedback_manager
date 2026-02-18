from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='pbkdf2_sha256$260000$reUsedLater$...') # Placeholder default to allow migration
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    createdAt = models.DateTimeField(auto_now_add=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.name
