from django.contrib import admin
from users.models import RedditUser
from reddit.admin import SubmissionInline

class RedditUserAdmin(admin.ModelAdmin):
    # Other configurations for RedditUserAdmin
    inlines = [SubmissionInline]

admin.site.register(RedditUser, RedditUserAdmin)
