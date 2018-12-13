from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.dateformat import format

from datetime import date, datetime

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
    #general fields
    dob = models.DateField(blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    hobbies = models.ManyToManyField(Hobby)
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True)

    def calc_age(self):
        today_date = date.today()
        return today_date.year - self.dob.year - ((today_date.month, today_date.day) < (self.dob.month, self.dob.day))

    def add_hobby(self, hobbyName):
        h = Hobby.objects.filter(name=hobbyName)
        if (h.count() != 0):
            h_obj = h.get()
            if (self.hobbies.filter(pk=h_obj.pk).exists() == False):
                self.hobbies.add(h_obj)

    def remove_hobby(self, hobbyName):
        h = Hobby.objects.filter(name=hobbyName)
        if (h.count() != 0):
            h_obj = h.get()
            if (self.hobbies.filter(pk=h_obj.pk).exists()):
                self.hobbies.remove(h_obj)       

    def as_json(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            dob=format(self.dob, 'dS M Y'),
            gender=self.get_gender_display(),
            hobbies=[h.name for h in self.hobbies.all()]
        )
    
    def hobbies_as_json(self):
        return dict(
            hobbies=[h.name for h in self.hobbies.all()]
        )

    def __str__(self):      
        return self.get_full_name()