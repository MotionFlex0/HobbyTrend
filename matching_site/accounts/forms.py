from django import forms

from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'dob', 'gender')