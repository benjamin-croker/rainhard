import datetime as dt

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from blog.models import Post, Tag, PostTag


def index(request):
    recent_posts = Post.objects.order_by('-pub_datetime')[:2]

    template = 'blog/index.html'
    context = {'recent_posts': recent_posts}

    return render(request, template, context)


def post(request, post_id):
    post = Post.objects.get(pk=int(post_id))

    template = 'blog/post.html'
    context = {'post': post}

    return render(request, template, context)


@login_required
def create(request):
    template = 'blog/create.html'
    return render(request, template)


def new(request):
    if (len(request.POST['post_content']) == 0 or
        len(request.POST['post_title']) == 0):
        # blank post, handle error
        return render(
            request, 'blog/create.html',
            context={'error_message': "Title and Content must be filled"}
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
            if t[0] == '#' and len(t) > 1]

    # get or create the tag objects then associate with the post
    for tag in tags:
        t, _ = Tag.objects.get_or_create(text=tag)
        t.save()
        pt = PostTag(post=p, tag=t)
        pt.save()
    print('done:)')
    # args must be iterable, so add the extra comma to the tuple
    return HttpResponseRedirect(reverse('blog:post', args=(p.id, )))


def testcurrentuser(request):
    return HttpResponse(request.user.username)
