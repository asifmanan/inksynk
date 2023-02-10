from django import forms
from classapp.models import Category, Tag


class SelectCategoryForm(forms.Form):
    selection = forms.BooleanField()

class CreateCategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(Category.objects.all(),empty_label="\ [Root Level]",required=False)
    class Meta:
        model = Category
        fields = ('parent','title','description')

class CreateTagForm(forms.ModelForm):
    parent = forms.ModelChoiceField(Tag.objects.all(),empty_label="\ [Root Level]",required=False)
    class Meta:
        model = Tag
        fields = ('parent','title','description')
        

        