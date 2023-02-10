from django.urls import path
from cmsapp import views

app_name = 'cmsapp'
urlpatterns=[
  path('home/',views.CMSHome.as_view(),name='cmshome'),
]