from django.contrib.auth import get_user_model
from django.db import models
from comments.models import Comment

class Submission(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    author = models.ForeignKey('users.RedditUser', on_delete=models.CASCADE, related_name='submitted_submissions')
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, related_name='submission_comments')

    def __str__(self):
        return f"<Submission:{self.id}>"

class RedditSubmission(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reddit_submissions')

    def __str__(self):
        return f"<RedditSubmission:{self.id}>"
