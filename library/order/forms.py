from django import forms
from book.models import Book
from authentication.models import CustomUser
from .models import Order


class OrderForm(forms.ModelForm):
    CHOICES = (('1 week', '1 week'),
               ('10 days', '10 days'),
               ('2 weeks', '2 weeks'),
               )
    book = forms.ModelChoiceField(label='',queryset= Book.objects.all().order_by('name'))
    user = forms.ModelChoiceField(label='',queryset= CustomUser.objects.all().order_by('email'))
    time = forms.ChoiceField(label='',  choices=CHOICES)

    class Meta:
        model = Order
        fields = 'book', 'user', 'time'


class OrderVisitorForm(forms.ModelForm):
    CHOICES = (('1 week', '1 week'),
               ('10 days', '10 days'),
               ('2 weeks', '2 weeks'),
               )
    book = forms.ModelChoiceField(label='', queryset= Book.objects.all().order_by('name'))
    time = forms.ChoiceField(label='',  choices=CHOICES)

    class Meta:
        model = Order
        fields = 'book', 'time'
