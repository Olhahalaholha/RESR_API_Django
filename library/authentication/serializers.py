"""
Serializers for authentication app
"""
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'email',
                  'password', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True,
                         'help_text': password_validation.password_validators_help_text_html()}
        }

    def validate_password(self, value):
        """
        Check that the password is valid.
        """
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        """Create and return user with encrypted password"""
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
