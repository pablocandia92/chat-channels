from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .forms import MessageForm

#@login_required
def chat_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    ctx = {
        'chat_messages' : chat_messages,
        'chat_form' : MessageForm
    }

    if request.method == 'POST':
        chat_form = MessageForm(request.POST)
        if chat_form.is_valid():
            chat_form.save(commit=False)
            chat_form.group = chat_group
            chat_form.author = request.user
            chat_form.save()
            

    return render(request, 'a_chat/chat.html', ctx)

