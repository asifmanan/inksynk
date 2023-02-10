from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, ListView
from django.http import HttpResponseRedirect
from django.contrib import messages
from classapp.forms import CreateCategoryForm, CreateTagForm, SelectCategoryForm
from classapp.models import Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from dashboard.views import AjaxableResponseMixin


# Create your views here.
class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    context_object_name = "category"
    template_name = 'adminapp/category_confirm_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def test_func(self):
        test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
        return test

class EditCategoryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'adminapp/create_category.html'
    success_url= reverse_lazy('adminapp:categories')

    def test_func(self):
        test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
        return test

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)


class CreateCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CreateCategoryForm
    template_name= 'adminapp/create_category.html'
    success_url= reverse_lazy('adminapp:categories')

    def test_func(self):
        test = self.request.user.groups.filter(name='administrator').exists() or self.request.user.is_superuser
        return test

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class CategoryList(LoginRequiredMixin, FormView):
    form_class=SelectCategoryForm
    template_name = 'adminapp/list_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = Category.objects.all()
        context['category_list']=category_list
        return context

class CategoryManager(LoginRequiredMixin, FormView):
    form_class = CreateCategoryForm
    template_name = 'classapp/categories1.html'
    success_url = reverse_lazy('classapp:categoriesmanager')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = Category.objects.all()
        context['category_list'] = category_list
        return context
    
    def form_valid(self, form):
        user = self.request.user
        category = form.save(commit=False)
        category.author = user
        form.save()
        messages.success(self.request, 'Your Category was published')
        print("Entry in category added successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category could not be published. Please try again')
        print("Unsuccessfull")
        # return HttpResponseRedirect(reverse('classapp:categorieshome'))
        return super().form_invalid(form)

class TagManager(LoginRequiredMixin, FormView):
    form_class = CreateTagForm
    template_name = 'classapp/tags1.html'
    success_url = reverse_lazy('classapp:tagsmanager')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_list = Tag.objects.all()
        context['tag_list'] = tag_list
        return context

    def form_valid(self,form):
        user = self.request.user
        tag = form.save(commit=False)
        tag.author = user
        form.save()
        messages.success(self.request, 'Your tag was published')
        print("form_valid")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request, 'Tag could not be published, try again')
        print("Form In-valid")
        return super().form_invalid(form)