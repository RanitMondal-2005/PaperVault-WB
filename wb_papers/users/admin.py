from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # This lets you see at a glance who needs help
    list_display = ['user', 'role', 'is_verified']
    list_filter = ['role', 'is_verified']
    
    # Simple action to verify faculty in one click
    actions = ['verify_faculty']

    def verify_faculty(self, request, queryset):
        queryset.update(is_verified=True)
    verify_faculty.short_description = "Approve Selected Faculty Members"