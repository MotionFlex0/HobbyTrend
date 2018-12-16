from django import forms

from .models import ProfileImage, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'dob', 'gender']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
    def __init__(self, *args, **kwargs):
        super(ProfileImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].initial = None # This disables the default image, for the PRofileImageForm