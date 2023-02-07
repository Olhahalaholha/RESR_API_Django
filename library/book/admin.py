"""
Admin for book
"""
from django.contrib import admin
from .models import Book
from author.models import Author


class BooksInfo(Book):

    class Meta:
        proxy = True
        verbose_name = 'Books info'
        verbose_name_plural = 'Books info'


class AuthorInline(admin.TabularInline):
    model = Author.books.through


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'book_authors']
    list_filter = ['name', 'id', 'authors']
    fields = ['name', 'description', 'count']
    search_fields = ['name']
    inlines = [AuthorInline]

    def book_authors(self, obj):
        result = '-'
        authors = obj.authors.all()
        if authors.exists():
            result = ','.join([str(x) for x in authors])
        return result


@admin.register(BooksInfo)
class BookAdmin2(admin.ModelAdmin):

    list_display = ['name', 'id', 'book_authors']
    list_filter = ['authors']
    search_fields = ['name']
    readonly_fields = ['name', 'book_authors', 'year_of_publication']

    fieldsets = (
        ('Note editable', {
            'fields': ('name', 'book_authors', 'year_of_publication')
        }),
        ('Editable', {
            'fields': ('date_of_issue',)
        })
    )

    def year_of_publication(self, obj):
        return obj.date_of_issue.year

    def book_authors(self, obj):
        result = '-'
        authors = obj.authors.all()
        if authors.exists():
            result = ','.join([str(x) for x in authors])
        return result
