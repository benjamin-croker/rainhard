from django.conf import settings 

# a context processor to add constants, like the site name
def add_constants(request):
    return {'blog_name': settings.BLOG_NAME}