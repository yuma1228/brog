from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import CreatePostForm


class ViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.post1 = Post.objects.create(title='User1の投稿', content='内容1', author=self.user1)
        self.post2 = Post.objects.create(title='User2の投稿', content='内容2', author=self.user2)

    def test_mypage_authentication(self):
        """MyPageViewはログインしていないとリダイレクトされるか"""
        response = self.client.get(reverse('brog:mypage'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/mypage/') 

    def test_mypage_displays_only_user_posts(self):
        """MyPageViewには自分の投稿だけが表示されるか"""
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('brog:mypage'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User1の投稿')  
        self.assertNotContains(response, 'User2の投稿')
    def test_create_post_view(self):
        """投稿が正しく作成されるか"""
        self.client.login(username='user1', password='password')
        
        response = self.client.post(reverse('brog:post_create'), {
            'title': '新しい投稿',
            'content': '新しい内容です。'
        })
        self.assertRedirects(response, reverse('brog:mypage'))
        self.assertTrue(Post.objects.filter(title='新しい投稿').exists())
        new_post = Post.objects.get(title='新しい投稿')
        self.assertEqual(new_post.author, self.user1)
        
class PostModelTest(TestCase):
    
    def test_post_creation_and_str(self):
        """ ポストが作成されるか"""
        user = User.objects.create_user(username='testuser', password='password')
        post = Post.objects.create(title='モデルテスト', content='内容', author=user)
        self.assertEqual(str(post), 'モデルテスト')
    
class CreatePostFormTest(TestCase):

    def test_form_valid(self):
        """フォーム作成がしっかりできるか"""
        form_data = {'title': '有効なタイトル', 'content': '有効な内容'}
        form = CreatePostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_no_title(self):
        """titleがないときエラーになるか"""
        form_data = {'title': '', 'content': 'タイトルがない'}
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_form_invalid_no_content(self):
        """内容ないときエラーになるか"""
        form_data = {'title': 'コンテントがない', 'content': ''}
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())
        

