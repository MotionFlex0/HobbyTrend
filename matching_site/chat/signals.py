from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, NewMessage

#This signal handler create a NewMessage for every user in the given CHat
@receiver(post_save, sender=Message)
def add_new_message(sender, instance, **kwargs):
    for p in instance.chat.participants.all():
        NewMessage(recipient=p, message=instance).save()
