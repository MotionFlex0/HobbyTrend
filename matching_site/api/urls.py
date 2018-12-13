from django.urls import path

from . import views

#URL patterns for /api/
urlpatterns = [
    path('getcommonusers', views.common_interest_users),
    path('user/me', views.me),
    path('user/me/hobbies', views.my_hobbies),
    path('user/<int:user_id>', views.user_req)
    #path('message/<int:recipient_id>', views.message)
]