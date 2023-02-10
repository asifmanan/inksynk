from django.urls import path
from siteapp.views import HomePage, PostView
app_name = 'siteapp'
urlpatterns = [
    path('',HomePage.as_view(),name='index'),
    path('<slug:slug>',PostView.as_view(),name='postview')
]