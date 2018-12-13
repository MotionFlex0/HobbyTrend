import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse

from accounts.models import UserProfile

from chat.models import Chat

def message(request, recipient_id):
    pass
    