from django.contrib import admin
from .models import College, Stream

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'university', 'slug')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    list_filter = ('college',)
    search_fields = ('name', 'college__name')