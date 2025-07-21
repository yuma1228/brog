from django.http import HttpResponse
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginForm, CreatePostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy


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
        context['all_posts'] =  Post.objects.all().order_by('-created_at')
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
        context['all_posts'] = Post.objects.all().order_by('-created_at')
        return context


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('brog:index')
    else:
        form = SignUpForm()
    
    return render(request, 'brog/signup.html', {'form': form})

class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = "brog/login.html"
class PostDetailView(DetailView):
    model = Post
    template_name = 'brog/post_detail.html'
    context_object_name = 'post'
    
class MyPageView(LoginRequiredMixin, ListView):
    paginate_by = 6
    model = Post
    template_name = 'brog/mypage.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'brog/post_create.html'
    success_url =  reverse_lazy('brog:mypage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'ポストが作成されました！')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '内容を正しく入力してください。')
        return super().form_invalid(form)




