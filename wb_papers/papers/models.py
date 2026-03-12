from django.db import models
from django.contrib.auth.models import User
from colleges.models import College, Stream

class Paper(models.Model):
    EXAM_TYPES = [
        ('INTERNAL', 'Internal / CA'),
        ('SEMESTER', 'Semester (End-Sem)'),
        ('PRACTICAL', 'Practical Exam'),
    ]
    
    title = models.CharField(max_length=200)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=[(i, f"Semester {i}") for i in range(1, 9)])
    year = models.IntegerField()
    subject_name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=20)
    # Fixed the choices reference below from LEFT_TYPES to EXAM_TYPES
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES) 
    pdf_file = models.FileField(upload_to='papers/%Y/%m/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} ({self.year})"