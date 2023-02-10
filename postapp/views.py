import re
from urllib import request
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from postapp.models import Post, PostCategory, PostTag, PostImage, PublishedPost, Approval, FeaturedPost
from classapp.models import Category, Tag
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, UpdateView, CreateView, DeleteView, DetailView
from postapp.forms import NewPostForm, PostCategoryForm, PostEditForm, PublishPostForm, PostApprovalForm, TagForm, PostImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from dashboard.views import AjaxableResponseMixin

# Create your views here.

class FeatureedPost(LoginRequiredMixin):
    pass


class CreatePostImage(LoginRequiredMixin, CreateView):
    form_class = PostImageForm
    template_name="postapp/upload_post_image.html"
    
    def form_valid(self, form):
        post=get_object_or_404(Post,pk=self.kwargs['post_pk'])
        form.instance.post=post
        return super().form_valid(form)

    def get_success_url(self):
        # success_url = super().get_success_url()
        success_url = reverse_lazy('postapp:editpost', kwargs={'pk':self.kwargs['post_pk']})
        return success_url
class PostApproval(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PostApprovalForm
    template_name='postapp/post_approval.html'
    success_url = reverse_lazy('postapp:listpostapproval')
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
        response = super().form_valid(form)
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
        return response

    def get_success_url(self):
        response = super().get_success_url()
        if Approval.Approved in self.request.POST:
            success_url = reverse_lazy('postapp:listpostapproval')
        return response
    


class UnpublishPost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PublishedPost
    context_object_name="ppost"
    success_url = reverse_lazy('postapp:draftposts')
    def test_func(self):
        try:
            post = self.get_object()
        except:
            print("Post Does not Exist")
            return False
        else:
            approved_test = not (post.approval == Approval.Approved)
            print(post.approval+" is type: "+str(type(post.approval)))
            print(Approval.Approved+" is type: "+str(type(Approval.Approved)))
            print(approved_test)
            test = (self.request.user == post.post.author and approved_test)
            return test

class DiscardDraft(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name="post"
    success_url = reverse_lazy('postapp:draftposts')
    def test_func(self):
        try:
            post = self.get_object()
        except:
            print("Post Does not Exist")
            return False
        else:
            test = (self.request.user == post.author)
            return test
class PublishPostView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = PublishedPost
    form_class = PublishPostForm
    template_name = 'postapp/publishpost.html'
    success_url = reverse_lazy('postapp:publishedposts')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(pk=self.kwargs['post_pk']).first()
        is_published = hasattr(post,'publishedpost')
        if is_published:
            post_tags = post.publishedpost.posttag.all()
            post_tag_ids = post_tags.values_list('tag_id', flat=True)
            context['form']['post_tags'].initial = post_tag_ids
            context['form']['post_category'].initial = post.publishedpost.postcategory.category
        return context

    def test_func(self):
        try:
            post = Post.objects.get(pk=self.kwargs['post_pk'])
        except:
            print("Post Does not Exist")
            return False
        else:
            is_approved = False
            is_published = hasattr(post,'publishedpost')
            if is_published:
                # print(post.publishedpost)
                if post.publishedpost.approval == Approval.Approved:
                    is_approved = True
            test = (self.request.user == post.author and not (post.title == "" and post.content == "") and not (is_approved))
            return test

    def form_valid(self,form):
        print("Form valid")
        try:
            post = Post.objects.get(pk=self.kwargs['post_pk'])
            published_post, created = PublishedPost.objects.get_or_create(post=post)
        except:
            print("form_invalid Returned")
            return super().form_invalid(form)
        else:
            # Model.objects.update_or_create(field1=val1, field2=val2, defaults={'field3': val3,'field4': val4})
            PostCategory.objects.update_or_create(ppost=published_post, defaults={'category': form.cleaned_data['post_category']})
            PostTag.objects.filter(ppost=published_post).delete()
            for post_tag in form.cleaned_data['post_tags']:
                PostTag.objects.create(ppost=published_post,tag=post_tag)          
            
            response = super().form_valid(form)
            return response
    
    def form_invalid(self,form):
        print("Form invalid")
        response = super().form_invalid(form)
        return response


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        existing_posts = Post.objects.filter(author=self.request.user,title="",summary="",content="")
        if len(existing_posts) < 5:
            newpost = Post(author=request.user)
            newpost.save()
        else:
            newpost = existing_posts.first()
        return redirect(reverse_lazy('postapp:editpost', kwargs={'pk':newpost.pk}))


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'postapp/editpost.html'
    success_url = reverse_lazy('postapp:draftposts')

    def test_func(self):
        try:
            post = self.get_object()
        except:
            print("Post Does not Exist")
            return False
        else:
            published = hasattr(post,'publishedpost')
            if published:
                print("Published")
            test = (self.request.user == post.author and not published)
            return test

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['postcategoryform'] = PostCategoryForm()
        context['tagform'] = TagForm()
        return context
    
    def form_valid(self,form):
        post=self.get_object()
        if 'publishpost' in self.request.POST:
            print("Publish")
            postcategoryform=PostCategoryForm(self.request.POST)
            tagform=TagForm(self.request.POST)
            if postcategoryform.is_valid() and tagform.is_valid():
                post_tag_objects = tagform.CreateTagFromTextInput(self,post)
                
                ppost, created = PublishedPost.objects.get_or_create(post=post,is_published=True)
                print("PublishedPostCreated: "+str(ppost))
                postcategory = postcategoryform.save(commit=False)
                postcategory.ppost = ppost
                postcategory.save()
                for posttag in post_tag_objects:
                    ptag, created = PostTag.objects.update_or_create(ppost=ppost,tag=posttag)
            else:
                form.save()
                return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self,form):
        response = super().form_invalid(form)
        print("Form is in-valid")
        return response

    def get_success_url(self):
        success_url = super().get_success_url()
        if "publishpost" in self.request.POST:
            success_url = reverse_lazy('postapp:publishedpost', kwargs={'pk':self.object.publishedpost.pk})
        return success_url

class PublishedPostView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PublishedPost
    template_name = 'postapp/view_publishedpost.html'
    def test_func(self):
        ppost = self.get_object()
        test = (self.request.user == ppost.post.author)
        return test



class ListPostApproval(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PublishedPost
    template_name = 'postapp/list_approval_posts.html'

    def test_func(self):
        test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
        return test

class ListApprovedPosts(LoginRequiredMixin, ListView):
    model = PublishedPost
    context_object_name = "approvedpost_list"
    template_name = 'postapp/list_approved_posts.html'

    def get_queryset(self):
        author = self.request.user
        approvedpost = PublishedPost.objects.filter(post__author=author,approval=Approval.Approved)
        return approvedpost

class ListDraftPosts(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'postapp/list_draft_posts.html'
    
    def get_queryset(self):
        author = self.request.user
        drafts = Post.objects.filter(author=author).exclude(publishedpost__is_published=True)
        return drafts

class ListPublishedPosts(LoginRequiredMixin, ListView):
    model = PublishedPost
    template_name = 'postapp/list_published_posts.html'
    
    def get_queryset(self):
        author = self.request.user
        return PublishedPost.objects.filter(post__author=author,is_published=True).exclude(approval=Approval.Approved)

