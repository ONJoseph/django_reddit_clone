from hashlib import md5
import mistune
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify  # Import slugify to generate a unique username

class RedditUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='', unique=True)  # Set a default value for the username field
    first_name = models.CharField(max_length=35, null=True, default=None, blank=True)
    last_name = models.CharField(max_length=35, null=True, default=None, blank=True)
    email = models.EmailField(null=True, blank=True, default=None)
    about = models.TextField(blank=True, null=True)
    about_text = models.TextField(blank=True, null=True, max_length=500, default=None)
    about_html = models.TextField(blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    gravatar_hash = models.CharField(max_length=32, null=True, blank=True, default=None)
    display_picture = models.BooleanField(null=True)
    homepage = models.URLField(null=True, blank=True, default=None)
    twitter = models.CharField(null=True, blank=True, max_length=15, default=None)
    github = models.CharField(null=True, blank=True, max_length=39, default=None)

    comment_karma = models.IntegerField(default=0)
    link_karma = models.IntegerField(default=0)

    # Use string-based import to break circular dependency
    submissions = models.ManyToManyField('submissions.Submission', related_name='submitted_users')
    comments = models.ManyToManyField('reddit.Comment', related_name='commenters', blank=True)

    def update_profile_data(self):
        self.about_html = mistune.markdown(self.about_text)
        if self.display_picture:
            self.gravatar_hash = md5(self.email.lower().encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        # Generate a unique lowercase username if it doesn't exist already
        if not self.username:
            self.username = slugify(self.user.username).lower()
        super(RedditUser, self).save(*args, **kwargs)

    def __str__(self):
        return "<RedditUser:{}>".format(self.user.username)
