from typing import Any
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import HttpResponse


def register(request):
    user_form = CustomUserCreationForm

    ctx = {
        'user_form' : user_form
    }

    if request.method == 'POST':
        user_form=CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            

            return HttpResponse('Registrado')
        
        else:
            #TODO return error message
            print(user_form.errors)

    return render(request, 'a_users/register_user.html', ctx)


class CustomLoginView(LoginView):
    template_name = 'a_users/login.html'
    form_class = CustomAuthenticationForm
    fields = '__all__'

    def get_success_url(self):
        print('aa')
        return reverse('chatroom', kwargs={'chatroom_name': 'public-chat'})
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            print('authenticado')
            return redirect(self.get_success_url())
        print('zzzz')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)
        ctx['user_form'] = ctx.pop('form', None)
        return ctx