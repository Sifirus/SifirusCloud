from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from users.models import Profile


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'full_name': 'Отображаемое имя',
            'bio': 'О себе',
            'location': 'Город',
            'avatar': 'Аватар'
        }
