from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from commentapp.models import Comment
from postapp.models import Approval
from commentapp.forms import CommentApprovalForm
# Create your views here.

class UserCommentList(LoginRequiredMixin, FormView):
  form_class = CommentApprovalForm
  template_name = 'commentapp/comment_list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comment_list'] = self.get_queryset()
    return context

  def get_queryset(self):
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
      qs = Comment.objects.filter(approval=approval,post__post__author=self.request.user).order_by('-updated_on')
    else:
      qs = Comment.objects.filter(post__post__author=self.request.user).order_by('-created_on')
    return qs

