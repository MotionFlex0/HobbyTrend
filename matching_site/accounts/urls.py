from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('imageUpload/', views.save_profile_image, name='imageUpload'),
    path('profile/', views.myprofile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]