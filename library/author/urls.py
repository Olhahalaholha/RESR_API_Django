from django.urls import path

from . import views 

app_name = 'authors'

urlpatterns = [
    path('all/', views.AuthorsList.as_view(), name='all'),
    path('new/', views.AddAuthor.as_view(), name='new'),
    path('delete/<int:author_id>/', views.delete_author, name='delete')
]