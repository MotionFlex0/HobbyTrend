from django.contrib import admin
from .models import Hobby, ProfileImage, UserProfile

# Register your models here.
admin.site.register(Hobby)
admin.site.register(ProfileImage)
admin.site.register(UserProfile)