from django.http import HttpResponse
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# ログイン前のトップページ
# ここでは、いまのところ全ての投稿を表示する

class IndexView(ListView):
    model = Post
    template_name = 'brog/index.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:3]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] =  Post.objects.all()
        return context
    

# ログイン後のトップページ
class HomeView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'brog/home.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:3]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'brog/post_detail.html'
    context_object_name = 'post'
    


# Create your views here.
