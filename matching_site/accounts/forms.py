from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'dob', 'gender', 'hobbies')