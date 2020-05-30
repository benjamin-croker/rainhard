from django.contrib import admin
from . import models

admin.site.register(models.Tag)
admin.site.register(models.PostTag)


class PostTagInline(admin.StackedInline):
    model = models.PostTag
    extra = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [PostTagInline]


admin.site.register(models.Post, PostAdmin)