from django import forms
from .models import Author
from book.models import Book


class AuthorForm(forms.ModelForm):
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    patronymic = forms.CharField(max_length=20)
    books = forms.ModelMultipleChoiceField(queryset= Book.objects.all())

    class Meta:
        model = Author
        fields = 'name', 'surname', 'patronymic'
        labels = {
            'name': 'Author Name:',
            'surname': 'Author Surname: ',
            'patronymic': 'Author Patronymic: '
        }
