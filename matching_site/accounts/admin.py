from django.contrib import admin
from .models import UserProfile, Hobby

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Hobby)