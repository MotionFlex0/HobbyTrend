from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Hobby

# Create your views here.

@login_required
def home(request):
    return render(request, 'core/home.html', {'hobby_list': Hobby.objects.all()})