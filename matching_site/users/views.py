from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Redirects user to login page (TODO: Only if they're not logged in)
def index(request):
    return HttpResponseRedirect('/accounts/login')