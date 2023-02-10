from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from classapp.models import Category, Tag
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.PROTECT)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL)
# remove blank = True "or not" from parent_id as per implementing logic
    title = models.CharField(max_length=96)
    summary = models.TextField(blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class PostMeta(models.Model):
    post = models.OneToOneField(Post,on_delete=models.CASCADE)
    key = models.CharField(max_length=100,blank=True)
    content = models.TextField(max_length=255,blank=True)
    def __str__(self):
        return self.key

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="postimage", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pictures',blank=True)
    image_caption = models.CharField(max_length=128,blank=True)
    def __str__(self):
        return self.image_caption

class Approval(models.TextChoices):
    Pending = 'PENDING', _('Pending')
    Disapproved = 'DISAPPROVED', _('Disapproved')
    Approved = 'APPROVED', _('Approved')
    
class PublishedPost(models.Model):
    post = models.OneToOneField(Post, related_name='publishedpost', on_delete=models.PROTECT)
    meta_title = models.CharField(max_length=96,blank=True)
    approval = models.CharField(max_length=11, choices=Approval.choices,default=Approval.Pending)
    approver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    published_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from="post", unique_with='published_on')
    def __str__(self):
        return self.post.title

class FeaturedPost(models.Model):
    ppost = models.OneToOneField(PublishedPost, on_delete=models.CASCADE,related_name="featured")
    featured = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ppost.post.title

class Relevance(models.IntegerChoices):
    MOST = 5, "Most Relevant"
    SOMEWHATMORE = 4, "Somewhat More Relevant"
    SOMEWHAT = 3, "Somewhat Relevant"
    SOMEWHATLESS = 2, "Somewhat Less Relevant"
    LEAST = 1, "Least Relevant"

class PostCategory(models.Model):
    ppost = models.OneToOneField(PublishedPost, on_delete=models.CASCADE,related_name='postcategory')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, related_name='postcategory')
    category_relevance = models.PositiveSmallIntegerField(
        choices=Relevance.choices,
        default=Relevance.SOMEWHAT
        )
    def __str__(self):
        return self.category.__str__()


class PostTag(models.Model):
    ppost = models.ForeignKey(PublishedPost,on_delete=models.CASCADE,related_name='posttag')
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name="posttag")
    tag_relevance = models.PositiveSmallIntegerField(
        choices=Relevance.choices,
        default=Relevance.SOMEWHAT
    )
    class Meta:
        unique_together = ['ppost','tag']
    def __str__(self):
        return self.tag.__str__()
