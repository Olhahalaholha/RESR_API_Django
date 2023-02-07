"""
Admin for author
"""
from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']
    filter_horizontal = ['books']
