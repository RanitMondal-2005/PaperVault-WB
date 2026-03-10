from django import models
from django import forms
from .models import Paper

class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'college', 'stream', 'semester', 'year', 'subject_name', 'exam_type', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.Select(attrs={'class': 'form-select'}),
            'stream': forms.Select(attrs={'class': 'form-select'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return file