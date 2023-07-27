from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'submission', 'created_at', 'updated_at']
    list_filter = ['user', 'submission', 'created_at', 'updated_at']
    search_fields = ['text', 'user__username', 'submission__title']
    ordering = ['-created_at']
