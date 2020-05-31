from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post, name='post'),
    # form for creating a new blog post
    path('create/', views.create, name='create'),
    # URL to POST data to
    path('new/', views.new, name='new'),
    # path('tags/', views.tags, name='tags'),
    # path('tags/<str:tag_id>/', views.tag, name='tag')
]
