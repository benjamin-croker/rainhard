import bleach
from bleach.css_sanitizer import CSSSanitizer
from django.db import models
from blog.html_whitelist import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    pub_datetime = models.DateTimeField(null=False)
    edit_datetime = models.DateTimeField(null=True, blank=True)

    @property
    def prev_post(self):
        try:
            return self.get_previous_by_pub_datetime()
        except self.DoesNotExist:
            return None
   
    @property
    def next_post(self):
        try:
            return self.get_next_by_pub_datetime()
        except self.DoesNotExist:
            return None
    
    @property
    def updated(self):
        # return the edit datetime, otherwise the publish time
        if self.edit_datetime:
            return self.edit_datetime
        return self.pub_datetime

    @property
    def tags(self):
        return [pt.tag for pt in self.posttag_set.all()]
    
    @property
    def tags_str(self):
        return " ".join([str(t) for t in self.tags])

    @property
    def cleaned_html(self):
        return bleach.clean(
            self.text,
            tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
            strip=True,
            css_sanitizer=CSSSanitizer(ALLOWED_STYLES)
        )
    
    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=256)

    def __str__(self):
        return f'#{self.text}'


class PostTag(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.post}: {self.tag}'
