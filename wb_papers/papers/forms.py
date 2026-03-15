import datetime
from django import forms
from .models import Paper
from django.core.validators import FileExtensionValidator # For PDF validation of Upload Form
from colleges.models import College, Stream

class PaperUploadForm(forms.ModelForm):
    # 1. Fixed Choices with Practical and empty placeholder for validation
    # FIX: Define Choices for dropdowns to replace standard number/text inputs
    EXAM_CHOICES = [
        ('', '--- Select Exam Type ---'),
        ('INTERNAL', 'Internal / CA'),
        ('SEMESTER', 'Semester (End-Sem)'),
        ('PRACTICAL', 'Practical Exam'),
    ]
    # 1.1: Update the stream field to use a custom label
    stream = forms.ModelChoiceField(
        queryset=Stream.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'}),
        empty_label="--- Select Stream ---"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1.2: FIX: Override the label display. 
        # This stops it from showing "Stream - College Name" and shows ONLY "Stream Name"
        self.fields['stream'].label_from_instance = lambda obj: f"{obj.name}"

    # 2. Created Dropdowns for Semester (1-8)
    SEM_CHOICES = [('', '--- Select Semester ---')] + [(i, f"Semester {i}") for i in range(1, 9)]
    
    # 3. Created Dropdowns for Year (Current to 2015)
    current_year = datetime.date.today().year
    YEAR_CHOICES = [('', '--- Select Year ---')] + [(r, r) for r in range(current_year, 2014, -1)]

    # 4. Define fields explicitly to force Dropdowns and 'Required' tooltips
    exam_type = forms.ChoiceField(
        choices=EXAM_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'})
    )
    semester = forms.ChoiceField(
        choices=SEM_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'})
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'})
    )
    # FIX: Added FileExtensionValidator to ensure only PDFs are accepted
    pdf_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': '.pdf'})
    )
    class Meta:
        model = Paper
        fields = ['title', 'college', 'stream', 'subject_name', 'subject_code', 'exam_type', 'year', 'semester', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures & Algorithm', 'required': 'true'}),
            'college': forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'}),
            'stream': forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'required': 'true'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': 'Enter Subject Name', 'required': 'true'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': 'e.g. CS-401', 'required': 'true'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
        }