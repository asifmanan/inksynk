from django.urls import path
from classapp import views

app_name = 'classapp'
urlpatterns = [
    path('categoriesmanager', views.CategoryManager.as_view(), name='categoriesmanager'),
    path('tagsmanager', views.TagManager.as_view(), name='tagsmanager'),
    
]