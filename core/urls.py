"""core URL Configuration

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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from django.conf.urls.static import static                      # used for static files


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='general/login.html'), name='login'),
    path('doc/', include('django.contrib.admindocs.urls'), name='admin_docs'),
    path('', admin.site.urls, name='admin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='general/logout.html'), name='logout'),
]