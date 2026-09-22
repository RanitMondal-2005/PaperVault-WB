"""
Users/models.py
"""
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [('STUDENT', 'Student'), ('FACULTY', 'Faculty')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    college = models.ForeignKey('colleges.College', on_delete=models.SET_NULL, null=True) # null=True allows a user to exist without being linked to a specific college and on_delete=models.SET_NULL ensures that if the college is deleted, the reference is set to NULL instead of deleting the user profile.
    # NOTE : This College field is not directly filled by the user during registration form fill up. Its handled by Admin based on the User's Faculty ID while verification process.
    is_verified = models.BooleanField(default=False) # For Faculty ID verification

    def __str__(self):
        return f"{self.user.username} ({self.role})"
