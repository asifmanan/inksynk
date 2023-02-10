import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# from postapp.models import PostCategory, Approval

# Create your models here.
class LowerCase(models.Transform):
    lookup_name = "lower"
    function = "LOWER"
    bilateral = True

models.CharField.register_lookup(LowerCase)
models.TextField.register_lookup(LowerCase)

class Category(models.Model):
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL)
    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=96, unique=True)
    meta_title = models.CharField(null=True, max_length=96)
    slug = models.SlugField()
    description = models.CharField(null=True, blank=True, max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        if not self.parent:
            return self.title
        title = self.title
        parent = self.parent
        while parent:
            title = parent.title + " -> " + title
            parent = parent.parent
        return title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        return super().save(*args,**kwargs)

    def parentlist(self):
        if not self.parent:
            return False
        parent_list = self.parent.title
        parent = self.parent.parent
        while parent:
            parent_list = parent.title + " > " + parent_list
            parent = parent.parent
        return parent_list


class Tag(models.Model):
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL)
    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=96, unique=True)
    meta_title = models.CharField(max_length=96)
    slug = models.SlugField()
    description = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        if not self.parent:
            return self.title
        title = self.title
        parent = self.parent
        while parent:
            title = parent.title + "-" + title
            parent = parent.parent
        return title

    def parentlist(self):
        if not self.parent:
            return False
        parent_list = self.parent.title
        parent = self.parent.parent
        while parent:
            parent_list = parent.title + " > " + parent_list
            parent = parent.parent
        return parent_list


