from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .models import Chat
from accounts.models import UserProfile

def logged_in_or_throw_exception(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied('You need to be logged in')
        else:
            return function(request, *args, **kwargs)
    return wrap

def does_chat_exist(function):
    @login_required
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
            raise PermissionDenied("You're not allowed access to this chat")
    return wrap