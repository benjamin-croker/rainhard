from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),

    # post list, defaults to page 1
    path('posts', views.all_posts, name='all_posts'),
    path('posts/<int:page_number>/', views.all_posts, name='all_posts'),

    # post list by tag, defaults to page 1
    path('posts/<str:tag_text>/', views.tag_posts, name='tag_posts'),
    path('posts/<str:tag_text>/<int:page_number>/', views.tag_posts, name='tag_posts'),

    # specific post
    path('post/<int:post_id>/', views.post, name='post'),
    # form for creating a new blog post
    path('accounts/create/', views.create, name='create'),
]
