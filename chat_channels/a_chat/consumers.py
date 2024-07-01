from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatGroup, GroupMessage
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name = self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)( #need to be async
            self.chatroom_name, self.channel_name #channel name identifies an unique user
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)( #need to be async
            self.chatroom_name, self.channel_name #channel name identifies an unique user
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body =text_data_json['body']

        message = GroupMessage.objects.create(
            body = body,
            author = self.user,
            group = self.chatroom
        )
        
        event = {
            'type' : 'message_handler',
            'message_id' : message.id
        }

        async_to_sync(self.channel_layer.group_send)( #group send replaces self.send
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)

        ctx = {
            'message' : message,
            'user' : self.user,
            'is_owner': message.author == self.user
        }

        html = render_to_string('a_chat/partials/user_message.html', context=ctx)


        self.send(text_data=html)