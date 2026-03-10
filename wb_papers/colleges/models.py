from django.db import models

class College(models.Model):
    UNIVERSITY_CHOICES = [
        ('MAKAUT', 'MAKAUT (formerly WBUT)'),
        ('JU', 'Jadavpur University'),
        ('CU', 'Calcutta University'),
        ('AUTONOMOUS', 'Autonomous Institution'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    university = models.CharField(max_length=20, choices=UNIVERSITY_CHOICES)
    logo = models.ImageField(upload_to='college_logos/', blank=True)

    def __str__(self):
        return self.name

class Stream(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=100) # e.g. CSE, IT, ECE, ME, CE

    def __str__(self):
        return f"{self.name} - {self.college.name}"