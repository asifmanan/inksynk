from django.contrib import admin
from commentapp.models import Comment, Commenter
# Register your models here.
admin.site.register(Comment)
admin.site.register(Commenter)
