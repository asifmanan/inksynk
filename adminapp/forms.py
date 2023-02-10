from django import forms
from commentapp.models import Comment


Approval = [
    ("APPROVED","Approve"),("DISAPPROVED","Disapprove")
]

class PostApprovalForm(forms.Form):
    approval = forms.ChoiceField(choices=Approval, widget=forms.RadioSelect)
    feature = forms.BooleanField(label='Feature this post',required=False)

class CommentApprovalForm(forms.Form):
    approval = forms.ChoiceField(choices=Approval,widget=forms.Select,)
    comment_approval = forms.BooleanField(widget=forms.CheckboxInput)
