from django.contrib import admin
from .models import College, Stream


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    search_fields = ('name',)
    list_filter = ('university',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')
    search_fields = ('name', 'college__name')
    list_filter = ('college',)
