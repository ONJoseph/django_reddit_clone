# Generated by Django 4.2.3 on 2023-07-27 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_reddituser_about_reddituser_avatar_and_more'),
        ('submissions', '0002_submission_author_submission_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_submissions', to='users.reddituser'),
        ),
    ]
