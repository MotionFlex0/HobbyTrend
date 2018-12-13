from django.http import HttpResponse, Http404
from django.shortcuts import render

from accounts.models import UserProfile

# Create your views here.
def conversation(request, user_id):
    try:
        r = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise Http404('Unknown user')
    return render(request, 'chat/chat.html', {'recipient':r.get_full_name()})