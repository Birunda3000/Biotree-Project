"""BioTree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.conf.urls.static import static
from BioTree import settings

from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='url_adm'),
    #user
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", profile, name='url_profile'),
    #local home+CRUD
    path('', home, name='url_home'),
    path('create/', create, name='url_create'),
    path('update/<int:pk>', update, name='url_update'),
    path('delete/<int:pk>', delete, name='url_delete'),
    # tree
    path('tree/', tree, name='url_tree'),
    path('dbaccess/', dbaccess, name='url_dbaccess'),
    path('about/', about, name='url_about'),
    path('tag_detail/<int:pk>', tag_detail, name='url_tag_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
