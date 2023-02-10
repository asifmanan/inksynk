from django import template
from postapp.models import Approval

register = template.Library()

@register.filter(name='catUserPostCount')
def catUserPostCount(postcategory, user):
  userpostcount = postcategory.filter(ppost__approval=Approval.Approved ,ppost__post__author=user).count()
  return userpostcount

@register.filter(name='tagUserPostCount')
def catUserPostCount(posttag, user):
  userpostcount = posttag.filter(ppost__approval=Approval.Approved ,ppost__post__author=user).count()
  return userpostcount

@register.filter(name='catTotalPostCount')
def catTotalPostCount(postcategory, category):
  totalpostcount = postcategory.filter(ppost__approval=Approval.Approved, category=category).count()
  return totalpostcount

@register.filter(name='tagTotalPostCount')
def tagTotalPostCount(posttag, tag):
  totalpostcount = posttag.filter(ppost__approval=Approval.Approved, tag=tag).count()
  return totalpostcount