from django.db import models
from django.contrib.auth.models import User

class Paper(models.Model):
    EXAM_TYPES = [
        ('INTERNAL', 'Internal / CA'),
        ('SEMESTER', 'Semester (End-Sem)'),
        ('PRACTICAL', 'Practical Exam'),
    ]

    title = models.CharField(max_length=200)

    college = models.ForeignKey('colleges.College', on_delete=models.CASCADE)
    stream = models.ForeignKey('colleges.Stream', on_delete=models.CASCADE)

    semester = models.IntegerField(choices=[(i, f"Semester {i}") for i in range(1, 9)]) # This creates a dropdown with options from Semester 1 to Semester 8 in the form.
    year = models.IntegerField()
    subject_name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    pdf_file = models.FileField(upload_to='papers/%Y/%m/') # Automatically groups files chronologically on the server file system (e.g., media/papers/2026/05/).
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Reference to the user who uploaded the paper is stored here so that we can track who uploaded each paper and null=True is used to allow for the possibility that the user may be delete the account but the paper remains.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} ({self.year})"
