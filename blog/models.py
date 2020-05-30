from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    pub_datetime = models.DateTimeField(null=False)
    edit_datetime = models.DateTimeField(null=True, blank=True)

    @property
    def prev_post(self):
        try:
            return self.get_previous_by_pub_datetime()
        except self.DoesNotExist:
            # TODO: consider if this is necessary here.
            # May end up just looking for a None anyway?
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

    
    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.CharField(max_length=256)

    def __str__(self):
        return f'#{self.text}'


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.post}: {self.tag}'
