"""
Admin for CustomUser
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .models import ROLE_CHOICES


FIELDSETS = (
        (None, {'fields': (
            'email', 'password', 'first_name', 'last_name', 'middle_name', 'role'
        )}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            'Important dates',
            {
                'fields': ('last_login', 'created_at', 'updated_at')
            }

        ),
    )

ADD_FIELDSETS = (
        (None, {'fields': (
            'email', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'role'
        )}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            'Important dates',
            {
                'fields': ('last_login', 'created_at', 'updated_at')
            }

        ),
    )

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'first_name', 'is_staff', 'user_role']
    fieldsets = FIELDSETS
    search_fields = ['email']

    add_fieldsets = ADD_FIELDSETS
    readonly_fields = ['last_login', 'created_at', 'updated_at']

    @admin.display(ordering='role')
    def user_role(self, obj):
        return ROLE_CHOICES[obj.role][1]



admin.site.register(CustomUser, UserAdmin)
