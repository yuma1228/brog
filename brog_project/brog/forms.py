from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from .models import Post

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']