from django import forms
from .models import User
import phonenumbers
from django_countries import countries
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(forms.ModelForm):
    modified_choices = [(code, f'{name} (+{phonenumbers.country_code_for_region(code)})') for code, name in countries]

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    country = forms.ChoiceField(choices = modified_choices, label="País") 


    class Meta:
        model = User
        fields = ['email', 'full_name', 'country' ,'phone']
        labels = {
            'email': 'Correo Electrónico',
            'full_name': 'Nombre Completo',
            'phone': 'Celular',
            'country': 'País',
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.initial['country'] = 'AR'

    def save(self, commit=True):
        user = super().save(commit=False)
        country_code = self.cleaned_data.get('country')
        phone = self.cleaned_data.get('phone')

        combined_phone = f"{country_code}{phone}"

        user.phone = combined_phone

        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    