from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
