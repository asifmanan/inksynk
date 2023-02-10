from django.db import models
from django.contrib.auth.models import User
from postapp.models import PublishedPost
from django.utils.translation import gettext_lazy as _

# Create your models here.

class FieldAttributes():
  commenter_NameMaxLength = 48
  commenter_EmailMaxLength = 144
  comment_ContentMaxLength = 1048

class Commenter(models.Model):
  name = models.CharField(max_length=FieldAttributes.commenter_NameMaxLength)
  email = models.EmailField(max_length=FieldAttributes.commenter_EmailMaxLength, unique=True)
  is_subscriber = models.BooleanField(default=False)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.name


class Approval(models.TextChoices):
  Pending = 'PENDING', _('Pending')
  Disapproved = 'DISAPPROVED', _('Disapproved')
  Approved = 'APPROVED', _('Approved')

class Comment(models.Model):
  parent = models.ForeignKey("self",null=True, blank=True, on_delete=models.CASCADE)
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
  commenter = models.ForeignKey(Commenter,null=True, blank=True, on_delete=models.SET_NULL)
  post = models.ForeignKey(PublishedPost, on_delete=models.CASCADE,related_name="Comments")
  content = models.CharField(max_length=FieldAttributes.comment_ContentMaxLength)
  approval = models.CharField(max_length=11, choices=Approval.choices,default=Approval.Pending)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.content




