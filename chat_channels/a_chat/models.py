from django.db import models
from a_users.models import User

class ChatGroup(models.Model):

    group_name = models.CharField(max_length=128, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):

    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author} - {self.body}'
    
    class Meta:
        ordering = ['-created']