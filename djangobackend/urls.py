"""
URL configuration for djangobackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from django.urls import re_path as url
from Infinitrax import views
import knox.views

urlpatterns = [
    re_path(r'^category$', views.categoryApi),
    re_path(r'^category/([0-9]+)$', views.categoryApi),
    re_path(r'^brand$', views.brandApi),
    re_path(r'^brand/([0-9]+)$', views.brandApi),
    re_path(r'^attribute$', views.attributeApi),
    re_path(r'^attribute/([0-9]+)$', views.attributeApi),
    re_path(r'^product$', views.productApi),
    re_path(r'^product/([a-zA-Z0-9]+)$', views.productApi), 
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login'),
    path('logout/', knox.views.LogoutView.as_view(), name='logout'),
    path('check/', views.check_user, name='check token'),
    path('user/', views.get_user, name='get user details'),
]

