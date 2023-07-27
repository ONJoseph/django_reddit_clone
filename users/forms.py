from django import forms
from django.contrib.auth.models import User
from users.models import RedditUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = RedditUser
        fields = ['first_name', 'last_name', 'about_html', 'homepage', 'twitter', 'github']
