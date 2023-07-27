from django.contrib import admin
from .models import Submission

# Register your models here.
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'user', 'score', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    ordering = ['-created_at']

