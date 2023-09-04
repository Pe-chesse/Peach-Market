from django.db import models
from user.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=32,primary_key=True)
    users = models.ManyToManyField(User,related_name='chatrooms', through='ChatRoomMember')
    last_message = models.ForeignKey('ChatMessage', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    num = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('chat_room', 'num')
        ordering = ['time']
    
    def __str__(self):
        return self.sender
        
class ChatRoomMember(models.Model):
    user = models.ForeignKey(User,related_name='membership', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    last_read = models.ForeignKey(ChatMessage, on_delete=models.SET_NULL, null=True, blank=True)
