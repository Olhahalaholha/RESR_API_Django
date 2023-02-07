"""
URLs mapping for book app
"""

from django.urls import path
from . import views


app_name = 'book'


urlpatterns = [
    path('', views.view_set, name='all'),
    path('<int:book_id>/', views.detail_view, name='detail'),
    path('search/', views.view_books_by_user, name='search'),
]