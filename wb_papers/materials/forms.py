import datetime
from django import forms
from .models import Material
from django.core.validators import FileExtensionValidator
from colleges.models import Stream


class MaterialUploadForm(forms.ModelForm):

    MATERIAL_TYPE_CHOICES = [
        ('', '--- Select Type ---'),
        ('NOTES', 'Notes'),
        ('ASSIGNMENT', 'Assignment / Teacher Suggestion'),
        ('PLACEMENT', 'Placement Notes'),
    ]

    SEM_CHOICES = [('', '--- Select Semester ---')] + [(i, f"Semester {i}") for i in range(1, 9)]

    material_type = forms.ChoiceField(
        choices=MATERIAL_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle', 'id': 'materialTypeSelect'})
    )

    stream = forms.ModelChoiceField(
        queryset=Stream.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'}),
        empty_label="--- Select Stream ---"
    )

    semester = forms.ChoiceField(
        choices=SEM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'})
    )

    pdf_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stream'].label_from_instance = lambda obj: f"{obj.name}"
        self.fields['college'].required = False

    def clean(self):
        cleaned_data = super().clean()
        material_type = cleaned_data.get('material_type')
        college = cleaned_data.get('college')
        stream = cleaned_data.get('stream')
        semester = cleaned_data.get('semester')

        # For non-placement types(like NOTES/ASSIGNMENT), college/stream/semester are required,
        # But For Placement Notes ,they are Optional
        if material_type != 'PLACEMENT':
            if not college:
                self.add_error('college', 'College is required for Notes and Assignments.')
            if not stream:
                self.add_error('stream', 'Stream is required for Notes and Assignments.')
            if not semester:
                self.add_error('semester', 'Semester is required for Notes and Assignments.')
        return cleaned_data

    class Meta:
        model = Material
        fields = ['title', 'material_type', 'college', 'stream', 'subject_name', 'semester', 'description', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures Notes Unit 1-3'}),
            'college': forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures & Algorithm'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional: briefly describe what this covers...'}),
        }