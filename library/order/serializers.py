"""
Serializers for order app
"""
from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'created_at', 'plated_end_at', 'end_at']
        read_only_fields = ['id', 'user', 'created_at']
        extra_kwargs = {
            'plated_end_at': {'required': True},
        }



class OrderAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'created_at', 'plated_end_at', 'end_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'plated_end_at': {'required': True},
        }
