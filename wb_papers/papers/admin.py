from django.contrib import admin
from .models import Paper 

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'college', 'stream', 'year', 'exam_type')
    list_filter = ('college', 'stream', 'exam_type', 'year')
    search_fields = ('subject_name', 'title')