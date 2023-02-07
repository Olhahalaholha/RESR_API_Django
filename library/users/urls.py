from django.urls import path

from . import views 

app_name = 'users'

urlpatterns = [
    path('all/', views.UsersList.as_view(), name='all'),
    path('view/<int:pk>/', views.UserProfile.as_view(), name='single')
]