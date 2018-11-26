from django.shortcuts import HttpResponse, render, redirect

from .forms import UserProfileForm

# This is the signup view
def signup(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # commit=False as we need to save the hashed password first
            profile.set_password(profile_form.cleaned_data['password'])
            profile.save()
            return redirect('home')
    else:
        profile_form = UserProfileForm()
    return render(request, 'registration/signup.html', {'form':profile_form})

def myprofile(request):
    return HttpResponse('My profile page')