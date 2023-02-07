"""
URLs mapping for authentication
"""

from django.urls import path
from . import views


app_name = 'authentication'


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]