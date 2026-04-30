from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from captcha.fields import CaptchaField

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    captcha = CaptchaField(label='Капча')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']