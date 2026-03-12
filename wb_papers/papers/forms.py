# from django import models
# from django import forms
# from .models import Paper

# class PaperUploadForm(forms.ModelForm):
#     class Meta:
#         model = Paper
#         fields = ['title', 'college', 'stream', 'semester', 'year', 'subject_name', 'exam_type', 'pdf_file']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'college': forms.Select(attrs={'class': 'form-select'}),
#             'stream': forms.Select(attrs={'class': 'form-select'}),
#             'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
#         }

#     def clean_pdf_file(self):
#         file = self.cleaned_data.get('pdf_file')
#         if not file.name.endswith('.pdf'):
#             raise forms.ValidationError("Only PDF files are allowed.")
#         return file

from django import forms
from .models import Paper, College

class PaperUploadForm(forms.ModelForm):
    EXAM_CHOICES = [('INTERNAL', 'Internal'), ('EXTERNAL', 'External')]
    
    exam_type = forms.ChoiceField(choices=EXAM_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    semester = forms.IntegerField(min_value=1, max_value=8, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 4'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}))
    
    class Meta:
        model = Paper
        fields = ['college', 'department', 'subject_name', 'subject_code', 'exam_type', 'year', 'semester', 'pdf_file']
        widgets = {
            'college': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS401'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }