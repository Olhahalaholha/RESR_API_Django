from django.urls import path, include
from . import views 


app_name = 'orders'


urlpatterns = [
    path('all/', views.OrderList.as_view(), name='all'),
    path('new/', views.OrderCreate.as_view(), name='new'),
    path('end/<int:order_id>/', views.end_order, name='end-order')
]