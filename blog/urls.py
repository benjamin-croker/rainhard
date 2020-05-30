from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post, name='post')
    # path('tags/', views.tags, name='tags'),
    # path('tags/<str:tag_id>/', views.tag, name='tag')
]
