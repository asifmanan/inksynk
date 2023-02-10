from django import forms
from commentapp.models import Commenter, Comment

Approval = [
    ("","Bulk Action"),("APPROVED","Approve"),("DISAPPROVED","Disapprove")
]

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('content',)

class CommenterForm(forms.ModelForm):
  class Meta:
    model = Commenter
    fields = ('name','email')

class CommentApprovalForm(forms.Form):
    approval = forms.ChoiceField(choices=Approval,widget=forms.Select)
    comment_approval = forms.BooleanField(widget=forms.CheckboxInput)
