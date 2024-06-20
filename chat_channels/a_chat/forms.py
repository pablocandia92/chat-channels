from django import forms
from .models import GroupMessage

class MessageForm(forms.ModelForm):
    
    class Meta:
        model = GroupMessage
        fields = ['body']
        labels = {
            'body' : 'Message'
        }
