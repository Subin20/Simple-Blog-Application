from django.urls import path
from .views import signup_view,profile_view
from . import views


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('posts/', views.view_posts, name='view_posts'),
    path('post/<int:pk>/', views.view_single_post, name='view_single_post'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),


]
