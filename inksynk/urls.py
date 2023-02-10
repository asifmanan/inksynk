"""inksynk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# for static files during deployment
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('site/admin', admin.site.urls),
    path('',include("siteapp.urls")),
    path('cms/',include("cmsapp.urls")),
    path('cms/user/',include("userapp.urls")),
    path('cms/post/',include("postapp.urls")),
    # path('cms/dashboard/',include("dashboard.urls")),
    path('cms/class/',include("classapp.urls")),
    path('cms/comments/',include("commentapp.urls")),
    path('cms/admin/',include("adminapp.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

