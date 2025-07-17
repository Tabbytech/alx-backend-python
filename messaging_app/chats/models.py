from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any additional fields you need here, for example:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    pass

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]
        return f"Conversation with: {', '.join(usernames)}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} in {self.conversation.id} at {self.timestamp}: {self.content[:50]}..."
