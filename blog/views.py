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
def all_posts(request, page_number=1):
    post_list = Post.objects.order_by('-pub_datetime')
    p = Paginator(post_list, 2)

    template = 'blog/all_posts.html'
    context = {'page_posts': p.page(int(page_number)).object_list,
               'page_number': page_number,
               'page_range': list(p.page_range)}

    return render(request, template, context)


# post for a specific tag
def tag_posts(request, tag_text, page_number=1):
    # check tag exists first
    tag = get_object_or_404(Tag, text=tag_text)
    post_pks = tag.posttag_set.values('post')
    post_list = Post.objects.filter(pk__in=post_pks).order_by('-pub_datetime')
    
    p = Paginator(post_list, 2)

    template = 'blog/tag_posts.html'
    context = {'page_posts': p.page(int(page_number)).object_list,
               'page_number': page_number,
               'page_range': list(p.page_range),
               'tag_text': tag_text}

    return render(request, template, context)


def post(request, post_id):
    post = get_object_or_404(Post, pk=int(post_id))

    template = 'blog/post.html'
    context = {'post': post}

    return render(request, template, context)


def about(request):
    template = 'blog/about.html'
    
    return render(request, template)


# redirects to the home page, but forces a login first
@login_required
def author(request):
    return HttpResponseRedirect(reverse('blog:index'))


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
    if not request.user.has_perms(['blog.add_post',
                                   'blog.add_tag',
                                   'blog.add_posttag']):
        return HttpResponseForbidden("Unauthorised")

    if request.method == 'GET':
        return _create_form(request)
    elif request.method == 'POST':
         return _create_handler(request)


def _update_form(request, post):
    return render(
        request, 'blog/update.html',
        context={'post': post, 'tiny_mce_url': settings.TINY_MCE_URL}
    )


def _update_handler(request, post):

    if (len(request.POST['post_content']) == 0 or
        len(request.POST['post_title']) == 0):
        
        # blank post, handle error
        return render(
            request, 'blog/update.html',
            context={'error_message': "Title and Content must be filled",
                     'post': post,
                     'tiny_mce_url': settings.TINY_MCE_URL}
        )

    # create the new post
    post.edit_datetime = dt.datetime.today()
    post.text = request.POST['post_content']
    post.title=request.POST['post_title']
    post.save()

    # Split tags on spaces.
    # Ignore tags not starting with '#' or tags == '#'
    # Remove '#' on valid tags
    tags = [t[1:] for t in request.POST['post_tags'].split(' ')
            if len(t) >= 2 and t[0] == '#']
    
    # delete all existing post-tag associations and re-create them
    post.posttag_set.all().delete()

    # get or create the tag objects then associate with the post
    for tag in tags:
        t, _ = Tag.objects.get_or_create(text=tag)
        t.save()
        pt = PostTag(post=post, tag=t)
        pt.save()
    # args must be iterable, so add the extra comma to the tuple
    return HttpResponseRedirect(reverse('blog:post', args=(post.id, )))


@login_required
def update(request, post_id):
    if not request.user.has_perms(['blog.change_post',
                                   'blog.add_tag',
                                   'blog.delete_posttag',
                                   'blog.add_posttag']):
        return HttpResponseForbidden("Unauthorised")

    post = get_object_or_404(Post, pk=int(post_id))

    if request.method == 'GET':
        return _update_form(request, post)
    elif request.method == 'POST':
         return _update_handler(request, post)
