"""
papers/forms.py
 - Paper Upload Form By Faculty
"""
import datetime
from django import forms
from .models import Paper
from django.core.validators import FileExtensionValidator
from colleges.models import Stream


class PaperUploadForm(forms.ModelForm):

    EXAM_CHOICES = [
        ('', '--- Select Exam Type ---'),
        ('INTERNAL', 'Internal / CA'),
        ('SEMESTER', 'Semester (End-Sem)'),
        ('PRACTICAL', 'Practical Exam'),
    ]

    SEM_CHOICES = [
        ('', '--- Select Semester ---'),
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]

    # ── Form fields ──

    stream = forms.ModelChoiceField(
        queryset=Stream.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select shadow-none border-primary-subtle',
            'id': 'uploadStreamSelect'
        }),
        empty_label="--- Select Stream ---"
    )

    exam_type = forms.ChoiceField(
        choices=EXAM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'})
    )

    semester = forms.ChoiceField(
        choices=SEM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'})
    )

    # year choices are empty here — We build the year dropdown dynamically in __init__ so it always shows the current year at the top without needing to update the code every year.
    year = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select shadow-none border-primary-subtle'})
    )

    pdf_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
    )

    def __init__(self, *args, **kwargs):

        # Call ModelForm's constructor to initialize self.fields and bind incoming data (POST/FILES) before modifying them below
        super().__init__(*args, **kwargs)

        # Show only stream name in dropdown (e.g. "CSE" instead of "CSE - Jadavpur University")
        self.fields['stream'].label_from_instance = lambda obj: obj.name

        # Build year dropdown from current year down to 2014
        current_year = datetime.date.today().year
        year_choices = [('', '--- Select Year ---')]

        for year in range(current_year, 2013, -1):
            year_choices.append((year, year))

        self.fields['year'].choices = year_choices


    # ── Server-side field validation ──

    def clean_exam_type(self):
        exam_type = self.cleaned_data.get('exam_type')
        valid = ['INTERNAL', 'SEMESTER', 'PRACTICAL']
        if not exam_type:
            raise forms.ValidationError("Please select an exam type.")
        if exam_type not in valid:
            raise forms.ValidationError("Invalid exam type selected.")
        return exam_type

    def clean_semester(self):
        semester = self.cleaned_data.get('semester')
        if not semester:
            raise forms.ValidationError("Please select a semester.")
        try:
            sem_int = int(semester)
        except (ValueError, TypeError):
            raise forms.ValidationError("Invalid semester value.")
        if sem_int not in range(1, 9):
            raise forms.ValidationError("Semester must be between 1 and 8.")
        return semester

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year:
            raise forms.ValidationError("Please select a year.")
        try:
            year_int = int(year)
        except (ValueError, TypeError):
            raise forms.ValidationError("Invalid year value.")
        current_year = datetime.date.today().year
        if not (2014 <= year_int <= current_year):
            raise forms.ValidationError(f"Year must be between 2014 and {current_year}.")
        return year

    def clean_pdf_file(self):
        pdf = self.cleaned_data.get('pdf_file')
        # NOTE : In Python and Django, pdf.size measures file size in bytes and returns an integer(raw bytes)...
        if pdf:
            # 5MB size limit server-side
            if pdf.size > 5 * 1024 * 1024: # 5MB in bytes -> 5,242,880 bytes
                raise forms.ValidationError("PDF file size must be under 5MB.")
            # Double-check extension server-side even though FileExtensionValidator exists
            if not pdf.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
        return pdf

    def clean_subject_code(self):
        code = self.cleaned_data.get('subject_code', '').strip()
        if not code:
            raise forms.ValidationError("Subject code is required.")
        # Subject codes should be reasonably short
        if len(code) > 20:
            raise forms.ValidationError("Subject code must be under 20 characters.")
        return code.upper()  # normalize to uppercase e.g. cs-401 → CS-401

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Paper title is required.")
        if len(title) < 3:
            raise forms.ValidationError("Title is too short.")
        return title


    # ----- Cross-field validation — runs after all individual clean_ methods ----
    def clean(self):
        cleaned_data = super().clean()
        college = cleaned_data.get('college')
        stream = cleaned_data.get('stream')

        # Ensure stream belongs to selected college (Although JS handles this in Frontend, Still a Final Check)
        if college and stream:
            if stream.college != college:
                raise forms.ValidationError(
                    "Selected stream does not belong to the selected college. "
                    "Please select a matching college and stream."
                )
        return cleaned_data

    class Meta:
        model = Paper
        fields = [
            'title', 'college', 'stream',
            'subject_name', 'subject_code',
            'exam_type', 'year', 'semester',
            'pdf_file'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Data Structures & Algorithm'
            }),
            'college': forms.Select(attrs={
                'class': 'form-select shadow-none border-primary-subtle',
                'id': 'uploadCollegeSelect' # <--- Sets id="uploadCollegeSelect", needed for JS
            }),
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Enter Subject Name'
            }),
            'subject_code': forms.TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'e.g. CS-401'
            }),
        }
