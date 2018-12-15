from django.core.exceptions import PermissionDenied
from django.http import Http404

from .models import Chat
from accounts.models import UserProfile

def does_chat_exist(function):
    def wrap(request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=kwargs['chat_id'])
            return function(request, *args, **kwargs)
        except Chat.DoesNotExist:
            raise Http404('This chat does not exist')
    return wrap


def is_user_chat_participant(function):
    @does_chat_exist
    def wrap(request, *args, **kwargs):
        chat = Chat.objects.get(id=kwargs['chat_id'])
        if request.user in chat.participants.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrap