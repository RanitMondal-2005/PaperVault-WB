from django.db import models

class College(models.Model):
    UNIVERSITY_CHOICES = [ # Hard-Coded Choices as Most WB Institutes fall under these or atmost Autonomous
        ('MAKAUT', 'MAKAUT (formerly WBUT)'),
        ('JU', 'Jadavpur University'),
        ('CU', 'Calcutta University'),
        ('AUTONOMOUS', 'Autonomous Institution'),
    ]

    name = models.CharField(max_length=255)
    university = models.CharField(max_length=20, choices=UNIVERSITY_CHOICES)
    logo = models.ImageField(upload_to='college_logos/', blank=True)

    class Meta:
        ordering = ['name'] # Automatically sorts colleges acc to their names alphabetically (A to Z) in DB

    def __str__(self):
        return self.name


class Stream(models.Model):
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name='streams'
    )
    name = models.CharField(max_length=100) # Stream branch name (e.g., CSE, IT, ECE)

    class Meta:
        ordering = ['name'] # Automatically sorts streams alphabetically (A to Z)
        unique_together = ('college', 'name') # Stop the same stream name from being added twice under the same college

    def __str__(self):
        return f"{self.name} - {self.college.name}"
