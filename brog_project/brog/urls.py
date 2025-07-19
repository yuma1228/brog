from django.urls import path,include
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'brog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('login/',LoginView.as_view(redirect_authenticated_user=True,template_name='brog/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
]
