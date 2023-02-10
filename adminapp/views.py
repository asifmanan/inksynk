from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from postapp.models import PublishedPost, FeaturedPost, Approval
from commentapp.models import Comment, Commenter
from adminapp.forms import PostApprovalForm, CommentApprovalForm
from django.utils.translation import gettext_lazy as _
# Create your views here.

class ListComment(LoginRequiredMixin, UserPassesTestMixin, FormView):
  form_class = CommentApprovalForm
  template_name = 'adminapp/list_comment.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    approval = self.kwargs['approval']
    if approval=="approved":
      approval = Approval.Approved
    elif approval == "pending":
      approval = Approval.Pending
    elif approval == "disapproved":
      approval = Approval.Disapproved
    else:
      approval = None
    if approval:
      context['comment_list'] = Comment.objects.filter(approval=approval).order_by('-updated_on')
    else:
      context['comment_list'] = Comment.objects.all().order_by('-created_on')
    return context

  def test_func(self):
    test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
    return test

  def form_valid(self,form):
    approval = form.cleaned_data['approval']
    item_list = self.request.POST.getlist('comment_approval')
    if approval=="APPROVED":
      approval=Approval.Approved
    elif approval=="DISAPPROVED":
      approval=Approval.Disapproved
    else:
      return super().form_invalid(form)
    print(item_list)
    comment_approval_list = Comment.objects.filter(id__in=item_list)
    for comment in comment_approval_list:
      comment.approval = approval
      comment.save()
      print("Comment is: "+str(comment.approval))
    return super().form_invalid(form)

class ListApprovedPost(LoginRequiredMixin, ListView, UserPassesTestMixin):
  model=PublishedPost
  template_name = 'adminapp/list_approved_post.html'
  context_object_name = 'approvedpost_list'

  def test_func(self):
    test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
    return test

  def get_queryset(self):
    approvedpost_list = PublishedPost.objects.filter(is_published=True,approval=Approval.Approved)
    return approvedpost_list

class ListDisapprovedPost(LoginRequiredMixin, ListView, UserPassesTestMixin):
  model=PublishedPost
  template_name = 'adminapp/list_disapproved_post.html'
  context_object_name = 'post_list'

  def test_func(self):
    test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
    return test

  def get_queryset(self):
    disapprovedpost_list = PublishedPost.objects.filter(is_published=True,approval=Approval.Disapproved)
    return disapprovedpost_list

class ListPendingPost(LoginRequiredMixin, ListView, UserPassesTestMixin):
  model = PublishedPost
  template_name = 'adminapp/list_pending_post.html'
  context_object_name = 'pendingpost_list'

  def test_func(self):
    test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
    return test

  def get_queryset(self):
    pendingpost_list = PublishedPost.objects.filter(is_published=True,approval=Approval.Pending)
    return pendingpost_list
  

class PostApproval(LoginRequiredMixin, UserPassesTestMixin, FormView):
  form_class = PostApprovalForm
  template_name='adminapp/post_approval.html'
  success_url = reverse_lazy('adminapp:listapprovedpost')
  # success_url = reverse_lazy('postapp:publishedposts')

  def test_func(self):
    test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
    return test
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    ppost = get_object_or_404(PublishedPost, pk=self.kwargs['pk'])
    context['ppost'] = ppost
    if context['ppost'].approval != 'PENDING':
      context['form']['approval'].initial=context['ppost'].approval
      print(type(context['form']['approval'].initial))
      try:
        if ppost.featured:
          pass
      except:
        print("Not Featured")

      else:
        if ppost.featured.featured==True:
          context['form']['feature'].initial=True
    # print("Before approval value in db: " + context['ppost'].approval)
    return context

  def form_valid(self,form):
    approval = form.cleaned_data['approval']
    feature = form.cleaned_data['feature']
    ppost = get_object_or_404(PublishedPost, pk=self.kwargs['pk'])
    is_featured=False
    try:
      fpost = ppost.featured
    except:
      print("Not Featured")
      fpost = False
    else:
      if fpost and fpost.featured:
        is_featured=True
      
      # print("Approval value returned: "+ approval)
    if approval==Approval.Approved:
      print("Approved (form)")
      if ppost.approval != Approval.Approved:
        ppost.approval = Approval.Approved
        ppost.approver = self.request.user
        ppost.save()
      if feature == True and not(is_featured):
        if not(fpost):
            fpost, created = FeaturedPost.objects.get_or_create(ppost=ppost)        
        fpost.featured=True
        fpost.save()
        print("Featured Post Set")
      elif feature == False and is_featured:
        fpost.featured = False
        fpost.save()

        # print("approval in db: " + ppost.approval)
      
    elif approval == Approval.Disapproved:
        if fpost:
          fpost.featured=False
          fpost.save()
        if ppost.approval != Approval.Disapproved:
          ppost.approval = Approval.Disapproved
          ppost.approver = self.request.user
          ppost.save()
        print("approval in db: " + ppost.approval)
    else:
      return super().form_invalid(form)
    return super().form_valid(form)

  def get_success_url(self):
    response = super().get_success_url()
    if Approval.Disapproved in self.request.POST['approval']:
      print("post is disapproved")
      response = reverse_lazy('adminapp:listdisapprovedpost')
    return response