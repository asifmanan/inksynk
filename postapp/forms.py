from django import forms
from postapp.models import Post, PostCategory, PostTag, PostImage
from classapp.models import Category, Tag
from django.core.exceptions import ObjectDoesNotExist
import re


Approval = [
    ("APPROVED","Approve"),("DISAPPROVED","Disapprove")
]

class PostImageForm(forms.ModelForm):
    class Meta:
        model=PostImage
        fields=('image','image_caption')

class PostApprovalForm(forms.Form):
    approval = forms.ChoiceField(choices=Approval, widget=forms.RadioSelect)
    feature = forms.BooleanField(label='Feature this post',required=False)

class PostCategoryForm(forms.ModelForm):
    class Meta:
        model=PostCategory
        fields=('category',)
        widgets = {'category':forms.Select(),}

class TagForm(forms.Form):
    tags = forms.CharField()
    
    def CreateTagFromTextInput(self, obj, post):
        tags = self.cleaned_data['tags']
        list1 = re.split(r'[,\s][\s|\n]*',tags)
        form_tag_list = list(filter(None,list1))
        
        post_tag_objects=[]
        for newtag in form_tag_list:
            try:
                tag = Tag.objects.get(title__lower=newtag)
            except ObjectDoesNotExist:
                tag = Tag(author=obj.request.user,title=newtag,description="First appeared in post: "+str(post.title))
                tag.save()
                post_tag_objects.append(tag)
            else:
                post_tag_objects.append(tag)
        return post_tag_objects

class PublishPostForm(forms.Form):
    post_category = forms.ModelChoiceField(label='Category',queryset=Category.objects.all(),empty_label="--Select Category--",required=True)
    post_tags = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(), 
        widget = forms.CheckboxSelectMultiple(),
    )


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','summary','content')
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'summary':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.TextInput(attrs={'class':'form-control'}),
        }

class PostEditForm(forms.ModelForm):
    # post_category = forms.ModelChoiceField(label='Category',queryset=Category.objects.all(),empty_label="--Select Category--",required=False)
    class Meta:
        model=Post
        fields=('title','summary','content')

