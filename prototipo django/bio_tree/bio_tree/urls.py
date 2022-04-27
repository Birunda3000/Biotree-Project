"""bio_tree URL Configuration

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
from ast import arg
from turtle import update
from django.contrib import admin
from django.urls import path, include
from numpy import delete

from home.views import home, argu, dashboard, tree, dbaccess, about, adicionar, update, delete

from django.conf import settings 
from django.conf.urls.static import static

from bio_tree import settings#***********


urlpatterns = [
    path('admin/', admin.site.urls, name="url_admin"),
    path('', home, name='url_home'),
    path('dashboard/', dashboard, name='url_dashboard'),
    path('tree/', tree, name='url_tree'),
    path('dbaccess/', dbaccess, name='url_dbaccess'),
    path('about/', about, name='url_about'),

    path('adicionar/', adicionar, name='url_adicionar'),

    path('update/<int:pk>/', update, name='url_update'),

    path('delete/<int:pk>/', delete, name='url_delete'),

    path('arg/<str:name>/<int:inteiro>', argu, name='url_argu'),

] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)   #depois do +

#path('', )