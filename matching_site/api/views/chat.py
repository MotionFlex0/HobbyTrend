import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse

from accounts.models import UserProfile
from chat.decorators import is_user_chat_participant
from chat.models import Chat, Message, NewMessage

# This view returns all the messages in a conversation. It also deletes any new messages for the authenticated user, related to that chat
@login_required
@is_user_chat_participant
def all_message(request, chat_id):
    if (request.method == 'GET'):
        senders = {}
        messages = {}

        chat = Chat.objects.get(id=chat_id)
        messages_query = Message.objects.filter(chat=chat).order_by('created_at')
        if messages_query != 0:
            sender_query = messages_query.values_list('sender', flat=True).distinct()
            for sender_id in sender_query:
                senders[sender_id] = UserProfile.objects.get(id=sender_id).as_json()
               
            message_counter = 0
            for message in messages_query.all():
                messages[message_counter] = message.as_json()
                message_counter += 1

            NewMessage.objects.filter(message__chat=chat, recipient=request.user).delete() # Anything here will already be included in the messages dict

            return JsonResponse(dict(
                message_count=message_counter,
                senders=senders,
                messages=messages
            ))                 
        else:
            return JsonResponse({})


# This view handles messages sent by a user.
@login_required
@is_user_chat_participant
def send_message(request, chat_id):
    if (request.method == 'POST'):
        if 'message' in request.POST:
            text = request.POST['message']
            new_message = Message(sender=request.user, text=text, chat=Chat.objects.get(id=chat_id)) #This is safe, as the checks whether the chat exists
            new_message.save() # A post_save signal handler will create a NewMessage obj for each user in the chat
            return JsonResponse({'success':1})

# This view responses with any new messages
@login_required
@is_user_chat_participant
def update_chat(request, chat_id):
    if (request.method == 'GET'):
        senders = {}
        messages = {}

        chat = Chat.objects.get(id=chat_id)
        new_messages_query = NewMessage.objects.filter(message__chat=chat, recipient=request.user).order_by('message__created_at')
        if new_messages_query.count() != 0:
            sender_query = new_messages_query.values_list('message__sender', flat=True).distinct()
            for sender_id in sender_query:
                senders[sender_id] = UserProfile.objects.get(id=sender_id).as_json()
            
            message_counter = 0
            for new_message in new_messages_query.all():
                messages[message_counter] = new_message.read().as_json()
                message_counter += 1

            return JsonResponse(dict(
                message_count=message_counter,
                senders=senders,
                messages=messages
            ))
        else:
            return JsonResponse({})
