import bleach

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'], 'img': ['src', 'alt']
}
ALLOWED_TAGS =  ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                 'em', 'i', 'li', 'ol', 'strong', 'ul', 'img',
                 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

def clean_post_html(post_text):
    return bleach.clean(
        post_text, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, strip=True
    )