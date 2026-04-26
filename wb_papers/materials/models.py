from django.db import models
from django.contrib.auth.models import User
from colleges.models import College, Stream


class Material(models.Model):
    MATERIAL_TYPES = [
        ('NOTES', 'Notes'),
        ('ASSIGNMENT', 'Assignment / Teacher Suggestion'),
        ('PLACEMENT', 'Placement Notes'),
    ]

    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='NOTES')
    # FIX: college and stream are optional for placement notes, as Placement Notes are Universal
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=200)
    semester = models.IntegerField(null=True, blank=True)
    pdf_file = models.FileField(upload_to='materials/%Y/%m/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.subject_name}"

    class Meta:
        ordering = ['-uploaded_at']