import datetime as dt

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from rainhard import settings
from blog.models import Post, Tag, PostTag


def index(request):
    # shows the most recent post
    recent_posts = Post.objects.order_by('-pub_datetime')[:1]

    if(len(recent_posts) >= 1):
        post = recent_posts[0]
    else:
        post = None

    template = 'blog/post.html'
    context = {'post': post}

    return render(request, template, context)


# all posts
def posts(request, page_number=1):
    p = Paginator(Post.objects.order_by('-pub_datetime'), 2)

    template = 'blog/posts.html'
    context = {'page_posts': p.page(int(page_number)).object_list,
               'page_number': page_number,
               'page_range': list(p.page_range)}

    return render(request, template, context)


def post(request, post_id):
    post = get_object_or_404(Post, pk=int(post_id))

    template = 'blog/post.html'
    context = {'post': post}

    return render(request, template, context)


def about(request):
    template = 'blog/about.html'
    
    return render(request, template)


def _create_form(request):
    return render(
        request, 'blog/create.html',
        context={'tiny_mce_url': settings.TINY_MCE_URL}
    )


def _create_handler(request):

    if (len(request.POST['post_content']) == 0 or
        len(request.POST['post_title']) == 0):
        
        # blank post, handle error
        return render(
            request, 'blog/create.html',
            context={'error_message': "Title and Content must be filled",
                     'tiny_mce_url': settings.TINY_MCE_URL}
        )

    # create the new post
    p = Post(
        pub_datetime=dt.datetime.today(),
        text=request.POST['post_content'],
        title=request.POST['post_title']
    )
    p.save()

    # Split tags on spaces.
    # Ignore tags not starting with '#' or tags == '#'
    # Remove '#' on valid tags
    tags = [t[1:] for t in request.POST['post_tags'].split(' ')
            if len(t) >= 2 and t[0] == '#']

    # get or create the tag objects then associate with the post
    for tag in tags:
        t, _ = Tag.objects.get_or_create(text=tag)
        t.save()
        pt = PostTag(post=p, tag=t)
        pt.save()
    # args must be iterable, so add the extra comma to the tuple
    return HttpResponseRedirect(reverse('blog:post', args=(p.id, )))


@login_required
def create(request):
    if not request.user.has_perm('blog.add_post'):
        return HttpResponseForbidden("Unauthorised")

    if request.method == 'GET':
        return _create_form(request)
    elif request.method == 'POST':
         return _create_handler(request)


@login_required
def new(request):
    if not request.user.has_perm('blog.add_post'):
        return HttpResponseForbidden("Unauthorised")

    