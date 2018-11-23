from django.shortcuts import render, redirect

from .forms import ProfileForm

# This is the signup view
def signup(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # commit=False as we need to save the hashed password first
            profile.set_password(profile_form.cleaned_data['password'])
            profile.save()
            return redirect('home')
    else:
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html', {'form':profile_form})