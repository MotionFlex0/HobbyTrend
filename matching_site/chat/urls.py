from django.urls import path

from . import views

#URL patterns for /api/
urlpatterns = [
    path('startchat/<int:user_id>', views.start_chat, name='startchat'),
    path('conversation/<int:chat_id>', views.conversation, name='conversation')
]