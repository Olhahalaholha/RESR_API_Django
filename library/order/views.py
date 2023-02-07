from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authentication.models import CustomUser
from book.models import Book 
from .models import Order 
from .forms import OrderForm, OrderVisitorForm
from .serializers import OrderSerializer, OrderAllSerializer


class OrderByUserAPIview(APIView):
    serializer_class = OrderSerializer

    def get_user(self, user_pk):
        try:
            return CustomUser.objects.get(pk=user_pk, is_superuser=False)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, user_pk):
        user = self.get_user(user_pk)
        orders = Order.objects.filter(user=user)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    def post(self, request, user_pk):
        user = self.get_user(user_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderByUserDetailAPIview(APIView):
    serializer_class = OrderSerializer

    def get_order(self, user_pk, order_pk):
        try:
            return Order.objects.get(id=order_pk, user_id=user_pk, is_superuser=False)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, user_pk, order_pk):
        order = self.get_order(user_pk, order_pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def put(self, request, user_pk, order_pk):
        order = self.get_order(user_pk, order_pk)
        serializer = self.serializer_class(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_pk, order_pk):
        order = self.get_order(user_pk, order_pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(APIView):
    serializer_class = OrderAllSerializer

    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderAllSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderAllSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    serializer_class = OrderAllSerializer

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = OrderAllSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk=None):
        queryset = self.get_object(pk)
        serializer = OrderAllSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, pk=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderList(generic.ListView, LoginRequiredMixin):
    
    model = Order 
    template_name = 'order/list.html'
    context_object_name = 'orders'
    
    def get_queryset(self, *args, **kwargs):
        request = self.request 
        orders = {
            0: Order.objects.filter(user=request.user),
            1: Order.objects.all()
        }
        return orders.get(request.user.role) # Order queryset varies depending on a user's role
    
    
class OrderCreate(generic.View, LoginRequiredMixin):
    
    def get(self, *args, **kwargs):
        request = self.request 
        if request.user.role != 1:
            form = OrderVisitorForm(request.POST or None)
        else:
            form = OrderForm(request.POST or None)
        
        book_qs = Book.objects.filter(count__gte=1)
        context = {
           'form': form,
           'books': book_qs,
            }
        return render(request, 'order/create_form.html', context)
    
    def post(self, *args, **kwargs):
        request = self.request
       
        if request.user.role != 1:
            form = OrderVisitorForm(request.POST or None)
        else:
            form = OrderForm(request.POST or None)

        if form.is_valid():
            book_obj = Book.objects.filter(name=form.cleaned_data['book']).first()
            if request.user.role != 1:
                user_obj = request.user
            else:
                user_obj = CustomUser.objects.filter(email=form.cleaned_data['user']).first()

            if form.cleaned_data['time'] ==  '1 week':
                order_term = timedelta(days=7) 
            elif form.cleaned_data['time'] ==  '10 days':
                order_term = timedelta(days=10) 
            elif form.cleaned_data['time'] ==  '2 weeks':
                order_term = timedelta(days=14) 

            order_end_date = timezone.now() + order_term 
            order_obj = Order.objects.create(
                user=user_obj,
                book=book_obj,
                plated_end_at=order_end_date
            )
            if book_obj.count >= 1:
                book_obj.count -= 1 
                book_obj.save()
            else:
                messages.warning(request, "Sorry, this book is not in stock.")
                return redirect('orders:new')
            messages.success(request, f"""Congratulations! A new order for book 
                                    {book_obj.name} has been created.""")
        return redirect('orders:all')    
    
    
@login_required
def end_order(request, order_id):
    if request.user.role != 1:
        messages.warning(request, "You don't have permissions for this action.")
        return redirect('orders:all')
    order_obj = get_object_or_404(Order, id=order_id)
    order_obj.end_at = timezone.now()
    order_obj.save()
    messages.success(request, f"{repr(order_obj)} has been ended.")
    return redirect('orders:all')
        

        
        
