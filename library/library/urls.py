"""library URL Configuration

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
from django.views.generic import TemplateView
from author.views import AuthorAPIView

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('books/', include('book.urls')),
    path('authors/', include('author.urls')),
    path('orders/', include('order.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api_v1.urls')),
]
