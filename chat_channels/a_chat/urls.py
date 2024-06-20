from django.urls import path
from .views import *

urlpatterns = [
    path('chat/room/<chatroom_name>', chat_view, name='chatroom'),
]