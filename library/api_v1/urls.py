"""
URL mapping for api v1 views
"""

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from author.views import AuthorAPIView, AuthorDetailAPIView
from book.views import TheBookApi, BookApi
from authentication.views import UserAPIView, UserDetailsAPIView
from order.views import OrderByUserAPIview, OrderByUserDetailAPIview, OrderAPIView, OrderDetailAPIView

app_name = 'api_v1'


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='api_v1:api-schema'),
        name='api-docs'
    ),

    path('author/', AuthorAPIView.as_view()),
    path('author/<int:author_id>', AuthorDetailAPIView.as_view()),
    path('order/', OrderAPIView.as_view(), name='orders_detail'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='orders'),
    path('user/', UserAPIView.as_view(), name='api-users'),
    path('user/<int:pk>/', UserDetailsAPIView.as_view(), name='api-user-detail'),
    path('user/<int:user_pk>/order/',
         OrderByUserAPIview.as_view(),
         name='api-orders-by-user'
         ),
    path('user/<int:user_pk>/order/<int:order_pk>/',
         OrderByUserDetailAPIview.as_view(),
         name='api-order-by-user'),
    path('book/',BookApi.as_view(),name='api-book'),
    path('book/<int:pk>/', TheBookApi.as_view(), name='api-book-detail'),

]
