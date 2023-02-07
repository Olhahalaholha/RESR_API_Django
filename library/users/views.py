from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required 

from authentication.models import CustomUser 
from order.models import Order 

# Create your views here.

class UsersList(generic.ListView, LoginRequiredMixin):
    
    model = CustomUser 
    template_name = 'users/list.html'
    context_object_name = 'users'
    
    
class UserProfile(generic.DetailView, LoginRequiredMixin):
    
    model = CustomUser 
    template_name = 'users/single.html'
    context_object_name = 'user'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = context['user']
        context['orders'] = user.order_set.all()
        return context
    

    


