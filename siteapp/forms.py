from django import forms
from commentapp.models import Comment, Commenter, FieldAttributes

class CommentForm(forms.Form):
  comment_content = forms.CharField(label="Comment",max_length=FieldAttributes.comment_ContentMaxLength)
  commenter_name = forms.CharField(label="Name",max_length=FieldAttributes.commenter_NameMaxLength)
  commenter_email = forms.EmailField(label="Email",max_length=FieldAttributes.commenter_EmailMaxLength)