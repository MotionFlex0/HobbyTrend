from django.contrib.auth.models import AbstractUser
from django.db import models

#This model is for all of our available hobbies
class Hobby(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='hobbies'

# This is the model each user 
class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    dob = models.DateField(blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    hobbies = models.ManyToManyField(Hobby)
    profile_pic = models.FileField(blank=True) 

    def __str__(self):      
        return self.username