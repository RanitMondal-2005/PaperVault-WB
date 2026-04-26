from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'college', 'stream', 'semester', 'uploaded_by', 'uploaded_at')
    list_filter = ('material_type', 'college', 'stream', 'semester')
    search_fields = ('title', 'subject_name')