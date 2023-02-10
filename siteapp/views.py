from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView
from postapp.models import PublishedPost, FeaturedPost, Approval
from commentapp.models import Commenter, Comment
from commentapp.forms import CommenterForm, CommentForm
from classapp.models import Category
from siteapp.forms import CommentForm
# from dashboard.views import AjaxableResponseMixin
# Create your views here.

class MenuContextDataMixin(object):
  """
  Mixing to add a persistant menu on the page.
  This mixin must be used on any view which renders menu
  """
  def get_context_data(self, **kwargs):
    context = super(MenuContextDataMixin,self).get_context_data(**kwargs)
    categories_main = Category.objects.all()[:3]
    categories_more = Category.objects.all()[3:]
    context['categories_main'] = categories_main
    context['categories_more'] = categories_more
    return context


class RelatedPostMixin(object):
  """
  Mixing to add a related posts to page.
  This mixin must be used on views used to display single post objects.
  """
  def get_context_data(self,**kwargs):
    ppost = kwargs.pop('ppost')
    related_category = ppost.postcategory.category
    related_tags = ppost.posttag.all()
    tags=[]
    
    for tag in related_tags:
      tags.append(tag.tag)
    
    related_post = PublishedPost.objects.filter(approval=Approval.Approved,postcategory__category=related_category).exclude(id=ppost.id) or PublishedPost.objects.filter(approval=Approval.Approved,posttag__tag__in=tags).exclude(id=ppost.id)
    
    context = super(RelatedPostMixin,self).get_context_data(**kwargs)
    context['related_posts'] = related_post
    return context


class HomePage(MenuContextDataMixin, ListView):
  model = PublishedPost
  template_name = 'siteapp/homepage.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    fposts = FeaturedPost.objects.filter(featured=True).order_by('-updated_on')[:2]
    fposts_ids = fposts.values_list('ppost_id', flat=True)
    pposts = PublishedPost.objects.filter(approval=Approval.Approved).order_by('-published_on').exclude(id__in=fposts_ids)
    if fposts or pposts:  
      context['featuredPosts'] = fposts
      context['PublishedPosts'] = pposts
    else: 
      context['undercontruction'] = True
    return context

  # def get_queryset(self):
  #   return PublishedPost.objects.filter(approval="APPROVED")

class PostView(MenuContextDataMixin, RelatedPostMixin, FormView):
  form_class = CommentForm
  template_name = 'siteapp/postview.html'
  
  def get_context_data(self, **kwargs):
    ppost = get_object_or_404(PublishedPost,approval=Approval.Approved, slug=self.kwargs['slug'])
    kwargs['ppost'] = ppost
    context = super().get_context_data(**kwargs)

    context['publishedpost'] = ppost
    if ppost.Comments:
      context['comments']=ppost.Comments.filter(approval=Approval.Approved)
    return context
  
  def form_valid(self, form):
    comment_content = form.cleaned_data['comment_content']
    commenter_name = form.cleaned_data['commenter_name']
    commenter_email = form.cleaned_data['commenter_email']

    post = PublishedPost.objects.get(slug=self.kwargs['slug'])
    commenter, created = Commenter.objects.update_or_create(email=commenter_email,defaults={'name':commenter_name})
    comment = Comment(content=comment_content,post=post, commenter=commenter)
    comment.save()
    
    return super().form_valid(form)

  def get_success_url(self,**kwargs):
    return reverse_lazy('siteapp:postview', kwargs={'slug':self.kwargs['slug']})