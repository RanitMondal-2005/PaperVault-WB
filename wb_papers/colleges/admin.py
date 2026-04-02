from django.contrib import admin
from .models import College

@admin.register(College)
class Admin(admin.ModelAdmin):
    search_fields=('name',)

