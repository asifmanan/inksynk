from django.contrib import admin
from postapp.models import Post, PostMeta, PostCategory, PostTag, PublishedPost
# Register your models here.
admin.site.register(Post)
admin.site.register(PostMeta)
admin.site.register(PostCategory)
admin.site.register(PostTag)
admin.site.register(PublishedPost)
