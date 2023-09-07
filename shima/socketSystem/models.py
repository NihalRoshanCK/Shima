from django.db import models

from userapp.models import Users


class Message(models.Model):
    MESSAGE_TYPE = [('text', 'text'), ('image', 'image'), ('video', 'video'), ('audio', 'audio'), ('file', 'file')]

    text = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=30, choices=MESSAGE_TYPE, default='text')
    media = models.ForeignKey(to='MessageMedia', on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sended_messages')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.created_at}'


class MessageMedia(models.Model):
    media = models.FileField(upload_to='media/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    


class NotificationContent(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.ForeignKey(NotificationContent, on_delete=models.CASCADE)
    is_seen=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}: {self.content__message}"