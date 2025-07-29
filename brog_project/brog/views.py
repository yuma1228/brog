from django.http import HttpResponse
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView,DeleteView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import SignUpForm, LoginForm, CreatePostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy,reverse


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
    form = CommentForm
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):   
        """ページ表示（GETリクエスト）の際に、テンプレートに渡すデータを追加するメソッド"""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """フォームが送信された（POSTリクエスト）際の処理を記述するメソッド"""
        self.object = self.get_object()
        form = CommentForm(request.POST, post=self.object, user=request.user)
        
        if form.is_valid():
            form.save()
            return redirect(self.object.get_absolute_url()) 
        else:
            context = self.get_context_data(object=self.object)
            context['form'] = form 
            return self.render_to_response(context)

    
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

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('brog:mypage') 
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'brog/post_detail.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('brog:post_detail', kwargs={'pk': self.kwargs['pk']})




