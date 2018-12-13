from django.urls import path

from . import views

#URL patterns for /api/
urlpatterns = [
    path('conversation/<int:user_id>', views.conversation)
]