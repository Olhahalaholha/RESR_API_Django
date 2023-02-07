"""
Admin for order
"""

from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user_email', 'plated_end_at']
    ordering = ['plated_end_at']


    @admin.display(ordering='user')
    def user_email(self, obj):
        return obj.user.email
