from django.contrib import admin
from django.urls import path
from userapp import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

app_name = 'userapp'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='userapp/login.html',redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('userprofile/<slug:slug>', views.UserProfileView.as_view(),name='userprofile'),
    
    # AJAX View for login status
    path('loginstatusquery/', views.LoginStatusQuery,name='loginstatusquery'),

    # AJAX View for user login using modal
    path('modallogin/', views.ModalLogin,name='modallogin'),
    
    # path('login',views.AuthorLogin.as_view(),name='login'),
]