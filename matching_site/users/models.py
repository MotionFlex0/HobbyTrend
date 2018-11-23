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
class Profile(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    #dob = models.DateField()
    #gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    #profile_image = models.FileField() # ImageField is best suited here but it requires Pillow(Image library for python)
    #hobbies = models.ManyToManyField(Hobby)

    def __str__(self):      
        return '{} {}'.format(self.first_name, self.last_name)