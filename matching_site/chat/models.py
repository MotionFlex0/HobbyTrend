from django.db import models

from accounts.models import UserProfile

class Chat(models.Model):
    participants = models.ManyToManyField(UserProfile)
    #admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #chat_name = models.CharField(max_length=200)

    def __str__(self):
        return ' | '.join([p.get_full_name() for p in self.participants.all()]) + ' (id: {})'.format(self.id)

class Message(models.Model):
    text = models.CharField(max_length=260)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
        
    def as_json(self):
        return dict(
            text=self.text,
            sender_id=self.sender.id,
            created_at=self.created_at
        )

# Is used to alert a user of any new message. Each instance is temporary
class NewMessage(models.Model):
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.message.text

    #This method return the message and  delete this instance
    def read(self):
        m = self.message
        self.delete()
        return m

    