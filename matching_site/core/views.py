from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Hobby

# This view shows the home page
@login_required
def home(request, *args):
    return render(request, 'core/home.html', {'hobby_list': Hobby.objects.all()})