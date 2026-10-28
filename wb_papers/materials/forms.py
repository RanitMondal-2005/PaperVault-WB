"""
materials/forms.py
- Materials Upload Form by Faculty
"""

from django import forms
from django.core.validators import FileExtensionValidator
from colleges.models import College, Stream
from .models import Material


class MaterialUploadForm(forms.ModelForm):

    # Dynamic choices: 1 to 8
    SEM_CHOICES = [('', '--- Select Semester ---')] + [(i, f"Semester {i}") for i in range(1, 9)]

    material_type = forms.ChoiceField(
        choices=[('', '--- Select Type ---')] + Material.MATERIAL_TYPES, # Bring & use the already defined Materials Choices in Models.py
        widget=forms.Select(attrs={
            'class': 'form-select shadow-none border-primary-subtle',
            'id': 'materialTypeSelect'
        })
    )

    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        required=False,  # Enforced conditionally in Material.clean()
        empty_label="--- Select College ---",
        widget=forms.Select(attrs={
            'class': 'form-select shadow-none border-primary-subtle',
            'id': 'uploadCollegeSelect'
        })
    )

    stream = forms.ModelChoiceField(
        queryset=Stream.objects.all(),
        required=False,  # Enforced conditionally in Material.clean()
        empty_label="--- Select Stream ---",
        widget=forms.Select(attrs={
            'class': 'form-select shadow-none border-primary-subtle',
            'id': 'uploadStreamSelect'
        })
    )

    semester = forms.TypedChoiceField(
        choices=SEM_CHOICES,
        coerce=int,
        # coerce=int: Converts the submitted value from a string to a real Python integer.
        # CAUSE: When an HTML dropdown is submitted, the browser always sends data as a string (e.g., <option value="3"> -> "3").
        # empty_value=None: Safely catches blank selections ('') and returns None instead of crashing int("").
        # NOTE ON PAPERS APP: In the papers app, this type conversion was manually handled in views.py (e.g., int(request.GET.get(...)) or ...is_digit() checks)
        # because papers lacked dedicated model-level clean() validation. Here in Materials, TypedChoiceField handles it cleanly upfront.
        # TypedChoiceField is a specialized version of a ChoiceField that automatically converts (coerces) the user's selected input value into a specific Python data type.
        empty_value=None,
        required=False,  # Enforced conditionally in Material.clean()
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'})
    )

    pdf_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
    )

    class Meta:
        model = Material
        fields = [
            'title',
            'material_type',
            'college',
            'stream',
            'subject_name',
            'semester',
            'description',
            'pdf_file'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Data Structures Notes Unit 1-3'
            }),
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Data Structures & Algorithms'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: briefly describe what this covers...'
            }),
        }
