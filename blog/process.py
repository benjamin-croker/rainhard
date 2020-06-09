import bleach
from blog.html_whitelist import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES

def clean_post_html(post_text):
    return bleach.clean(
        post_text,
        ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES,
        strip=True
    )