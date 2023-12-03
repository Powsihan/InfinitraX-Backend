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
from django.urls import path
from django.urls import re_path as url
from Infinitrax import views
import knox.views

urlpatterns = [
    url(r'^category$',views.categoryApi),
    url(r'^category$',views.categoryApi),
    url(r'^category/([0-9]+)$',views.categoryApi),
    url(r'^brand$',views.brandApi),
    url(r'^brand$',views.brandApi),
    url(r'^brand/([0-9]+)$',views.brandApi),
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login'),
    path('logout/', knox.views.LogoutView.as_view(), name='logout'),
    path('check/', views.check_user, name='check token')
]

