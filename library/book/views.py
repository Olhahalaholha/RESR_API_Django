"""
Views for book
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from .models import Book
from author.models import Author
from order.models import Order
from django.http import HttpResponseForbidden, Http404
from authentication.models import CustomUser
from authentication.forms import SearchUserById
from .serializers import BookSerializer


class BookApi(APIView):
    serializer_class = BookSerializer

    def get(self, request):
        return Response(BookSerializer(Book.objects.all().order_by('pk'), many=True).data,
                        status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TheBookApi(APIView):
    serializer_class = BookSerializer

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk=pk)
        return Response(BookSerializer(book).data)

    def put(self, request, pk):

        book = self.get_object(pk=pk)
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required()
def view_set(request):
    """All books view"""
    filter_data = dict()
    books = Book.objects.all()

    if request.GET.get('author'):
        try:
            filter_data['author'] = int(request.GET.get('author'))
        except ValueError as e:
            print(e)
        else:
            books = books.filter(authors__in=[filter_data['author']])
    if request.GET.get('book'):
        try:
            filter_data['book'] = int(request.GET.get('book'))
        except ValueError as e:
            print(e)
        else:
            books = books.filter(pk=filter_data['book'])

    authors = Author.objects.filter(books__in=books).distinct()

    return render(request, 'book/all.html', {'books': books,
                                             'authors': authors,
                                             'filter_data': filter_data})


@login_required()
def detail_view(request, book_id):
    """Detail book view"""
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/detail.html', {'book': book})


@login_required()
def view_books_by_user(request):
    """All books by user view - only for librarian"""
    if request.user.role != 1:
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = SearchUserById()
        return render(request, 'book/book_by_user.html', {'search_form': form})

    if request.method == 'POST':
        form = SearchUserById(request.POST)
        res = ''
        search_query = ''
        if form.is_valid():
            search_query = form.cleaned_data['user_id']
            res = Order.objects.filter(user__pk=search_query) \
                .select_related('book').order_by('-end_at')

        return render(request, 'book/book_by_user.html',
                      {'search_query': search_query,
                       'orders': res,
                       'search_form': form})
