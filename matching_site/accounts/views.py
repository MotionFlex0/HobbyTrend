from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm

# This is the signup view

def register(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        print(profile_form.data["dob"])
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # commit=False as we need to save the hashed password first
            profile.set_password(profile_form.cleaned_data['password'])
            profile.save()
            new_user = authenticate(username=profile_form.cleaned_data['username'], password=profile_form.cleaned_data['password'])
            login(request, new_user)
            return redirect('home')
    else:
        profile_form = UserProfileForm()
    return render(request, 'accounts/login.html', {'form':profile_form})

def login_view(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user =  authenticate(request, username=username,  password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'username':username})
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def save_profile_image(request):
    if request.method == 'POST':
        return redirect('')
    else:
        return redirect('')


@login_required
def myprofile(request):
    return render(request, 'accounts/my_profile.html')