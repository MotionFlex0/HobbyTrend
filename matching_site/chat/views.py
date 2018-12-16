from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render

from accounts.models import UserProfile
from .models import Chat
from .decorators import is_user_chat_participant

#Starts a new chat with a user (if one does not already exist)
@login_required
def start_chat(request, user_id):
    try:
        user2 = UserProfile.objects.get(id=user_id)
        if (request.user != user2):
            chat = Chat.objects.filter(participants=request.user).get(participants=user2)
        else:
            raise Http404('You cannot start a chat with yourself')

    except UserProfile.DoesNotExist:
        raise Http404('This user does not exist')
    except Chat.DoesNotExist:
        chat = Chat()
        chat.save() 
        chat.participants.add(request.user, user2)

    return redirect('conversation', chat_id=chat.id)

#Renders the chat window using the chat id
@login_required
@is_user_chat_participant
def conversation(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    other_users = chat.participants.exclude(pk=request.user.pk)
    if (other_users.count() > 0):
        user2 = other_users[0]
    else:
        chat.delete()
        raise Http404('This chat has now been deleted, as you were the only participant.')
    return render(request, 'chat/chat.html', {'chat_id':chat_id, 'recipient_name':user2.get_full_name(), 'recipient_username':user2.username})