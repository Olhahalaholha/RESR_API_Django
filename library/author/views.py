import logging

from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author
from book.models import Book
from .forms import AuthorForm
from .serializers import AuthorSerializer
# Create your views here.

# from rest_framework import generics
# class AuthorAPIView(generics.ListAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

class AuthorAPIView(APIView):
    serializer_class = AuthorSerializer
    def get(self, request):
        res = Author.objects.all()
        print(AuthorSerializer(res, many=True).data, type(AuthorSerializer(res, many=True).data))
        return Response({'data': AuthorSerializer(res, many=True).data})

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logging.warning(f'AFTER  VALIDATION SERIALIZER {serializer=} ')
        serializer.save()
        logging.warning(f'AFTER  VALIDATION SERIALIZER {serializer=} ')
        print(serializer.data.get('id'))
        return Response(serializer.data, status=201)


class AuthorDetailAPIView(APIView):
    serializer_class = AuthorSerializer
    def get(self, request, *args, **kwargs):
        author_id = kwargs.get("author_id", None)
        if not author_id:
            return Response({'error': f'{author_id=} is not defined'}, status=422)
        try:
            author = Author.objects.get(pk=author_id)
        except:
            return Response({'error': f'{author_id=} not found'}, status=404)

        return Response({'data': AuthorSerializer(author).data})

    def patch(self, request, *args, **kwargs):
        author_id = kwargs.get("author_id", None)
        if not author_id:
            return Response({'error': f'{author_id=} is not defined'}, status=422)
        try:
            author = Author.objects.get(pk=author_id)
        except:
            return Response({'error': f'{author_id=} not found'}, status=404)

        serializer = AuthorSerializer(instance=author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        author_id = kwargs.get("author_id", None)
        if not author_id:
            return Response({'error': f'{author_id=} is not defined'}, status=422)
        try:
            author = Author.objects.get(pk=author_id)
        except:
            return Response({'error': f'{author_id=} not found'}, status=404)

        if author.books.count() == 0:
            author.delete()
            return Response(status=204)
        else:
            return Response({'error': f'Author have books.'},  status=422)



class AuthorsList(generic.View, LoginRequiredMixin):
    
    def get(self, *args, **kwargs):
        request = self.request 
        if request.user.role != 1:
            messages.warning(request, "You have no permissions to view this page.")
            return redirect('/')
        else:
            return render(request, 'author/list.html', {'authors': Author.objects.all()})
        
        
class AddAuthor(generic.View, LoginRequiredMixin):
    
    def get(self, *args, **kwargs):
        request = self.request 

        if request.user.role != 1:
            messages.warning(request, "You have no permissions to view this page.")
            return redirect('/')
        else:
            form= AuthorForm()
            context = {
                'form': form,
            }
            return render(request, 'author/create_form.html', context)
        
    def post(self, *args, **kwargs):    
        request = self.request 
        form = AuthorForm(request.POST)
        if form.is_valid():

            author_data = {
                'name': form.cleaned_data['name'],
                'surname': form.cleaned_data['surname'],
                'patronymic': form.cleaned_data['patronymic']
            }
        
            book_ids = form.cleaned_data['books']      
            books = Book.objects.filter(id__in=book_ids)
            form.save()

            author_obj = Author.objects.create(**author_data)
            author_obj.books.set(books)
            messages.success(request, f"""{author_data['surname']} {author_data['name']}
                                      {author_data['patronymic']} has been added to 
                                      authors! Check it out!""")
        return redirect('authors:all')
        
        
@login_required 
def delete_author(request, author_id):
    if request.user.role != 1:
        messages.warning(request, "You have no permissions for this action.")
        return redirect('/')
    author_obj = get_object_or_404(Author, id=author_id)
    author_obj.delete()
    messages.success(request, f"{author_obj.name}(id={author_obj.id}) has been deleted.")
    return redirect('authors:all')
    