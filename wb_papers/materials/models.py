from django.db import models
from django.contrib.auth.models import User
from colleges.models import College, Stream


class Material(models.Model):
    MATERIAL_TYPES = [
        ('NOTES', 'Notes'),
        ('ASSIGNMENT', 'Assignment / Teacher Suggestion'),
        ('LAB_MANUAL', 'Lab Manual'),
        ('PLACEMENT', 'Placement Notes'),
    ]

    # Derive max_length from the longest choice key — future-proof
    MATERIAL_TYPE_MAX_LENGTH = max(len(key) for key, _ in MATERIAL_TYPES) # among the present choices of materials,the max length will be the highest length choice characters

    title = models.CharField(max_length=200)

    material_type = models.CharField(
        max_length=MATERIAL_TYPE_MAX_LENGTH,
        choices=MATERIAL_TYPES,
        default='NOTES'
    )

    # Placement Notes are universal — no college/stream needed
    # Notes, Assignments, Lab Manuals are college-specific — required
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    subject_name = models.CharField(max_length=200)

    # Semesters 1-8 (optional for placement notes, mandatory otherwise)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)

    pdf_file = models.FileField(upload_to='materials/%Y/%m/')

    # SET_NULL instead of CASCADE — if faculty account is deleted,
    # their uploaded materials remain accessible to students
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    # blank=True only — Django stores empty string, not NULL for TextFields
    description = models.TextField(blank=True, default='')

    # -------- VALIDATIONS ---------------------------------------

    # Instead of Writing individual validations in each form, we directly wrote in models.py as universal validation
    def clean(self):
        from django.core.exceptions import ValidationError

        if self.material_type != 'PLACEMENT':
            if not self.college:
                raise ValidationError({
                    'college': 'College is required for Notes, Assignments, and Lab Manuals.'
                })
            if not self.stream:
                raise ValidationError({
                    'stream': 'Stream is required for Notes, Assignments, and Lab Manuals.'
                })
            if not self.semester:
                raise ValidationError({
                    'semester': 'Semester is required for Notes, Assignments, and Lab Manuals.'
                })

        if self.semester is not None:
            if not (1 <= self.semester <= 8):
                raise ValidationError({
                    'semester': 'Semester must be between 1 and 8.'
                })

        if self.college and self.stream:
            if self.stream.college != self.college:
                raise ValidationError({
                    'stream': 'Selected stream does not belong to the selected college.'
                })

    def __str__(self):
        return f"{self.title} — {self.subject_name}"

    class Meta:
        ordering = ['-uploaded_at']
