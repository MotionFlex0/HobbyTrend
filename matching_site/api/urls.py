from django.urls import path

from . import views

#URL patterns for /api/
urlpatterns = [
    path('accounts/upload_image', views.upload_profile_image),
    path('chat/<int:chat_id>/allmessages', views.all_message), #Get all messages
    path('chat/<int:chat_id>/send', views.send_message), #Send a message to all users in a chat
    path('chat/<int:chat_id>/update', views.update_chat), #Check if there are any new messages
    path('getcommonusers', views.common_interest_users),
    path('user/me', views.me),
    path('user/me/hobbies', views.my_hobbies),
    path('user/<int:user_id>', views.user_req),
]