from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render, redirect

from .models import ProfileImage
from .forms import UserProfileForm

# This is the register view. When a GET/POST is sent to this view, it will either show the register page or register the user
def register(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # commit=False as we need to save the hashed password first
            profile.set_password(profile_form.cleaned_data['password'])
            
            try:
                new_pic = ProfileImage.objects.get(image=request.POST['image_name'])
            except ProfileImage.DoesNotExist:
                new_pic = ProfileImage()
                new_pic.save()     
            profile.profile_pic = new_pic
            profile.save()

            new_user = authenticate(username=profile_form.cleaned_data['username'], password=profile_form.cleaned_data['password'])
            login(request, new_user)
            return redirect('home')
    else:
        profile_form = UserProfileForm()
    return render(request, 'accounts/login.html', {'form':profile_form})

# This view is displayed to the user, when they go to accounts/login. If their credentials are corret, they're redirect to the home page
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

# View for when the user logs out
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')