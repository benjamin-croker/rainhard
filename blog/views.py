from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from blog.models import Post


def index(request):
    recent_posts = Post.objects.order_by('-pub_datetime')[:2]

    template = 'blog/index.html'
    context = {'recent_posts': recent_posts}

    return render(request, template, context )


def post(request, post_id):
    post = Post.objects.get(pk=int(post_id))

    template = 'blog/post.html'
    context = {'post': post}

    return render(request, template, context )
    
