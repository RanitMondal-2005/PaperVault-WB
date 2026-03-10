from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [('STUDENT', 'Student'), ('FACULTY', 'Faculty')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    college = models.ForeignKey('colleges.College', on_delete=models.SET_NULL, null=True)
    is_verified = models.BooleanField(default=False) # For Faculty ID verification

    def __str__(self):
        return f"{self.user.username} ({self.role})"