from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = User