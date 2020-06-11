"""library_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('', index),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('reader/', reader_index, name='reader'),
    path('reader/account', reader_account, name='reader_account'),
    path('reader/lend', reader_lend, name='reader_lend'),
    path('reader/history', reader_history, name='reader_history'),
    path('manager/', manager_lend, name='manager'),
    path('manager/lend', manager_lend, name='manager_lend'),
    path('manager/book', manager_book, name='manager_book'),
    path('manager/enter', manager_enter, name='manager_enter'),
    path('manager/delete', manager_delete, name='manager_delete'),
    path('manager/lendinfo', manager_lend_info, name='manager_lend_info'),
    path('book/<str:isbn>', book, name='book'),
]
