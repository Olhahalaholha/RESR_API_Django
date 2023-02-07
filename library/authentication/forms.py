"""
Forms for authentication app
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth import get_user_model


def validate_user_id(value):
    user = CustomUser.objects.filter(pk=value).first()
    if not user:
        raise ValidationError(
            'User with id %(user_id)s does not exists.',
            params={'user_id': value}
        )


class SearchUserById(forms.Form):
    user_id = forms.IntegerField(required=True,
                                 error_messages={
                                     'invalid': 'To search for books by a specific user,'
                                                ' only the user number is available.'},
                                 label='Enter user id',
                                 validators=[validate_user_id],
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Enter user id'
                                     }))


class CustomAuthenticationForm(AuthenticationForm):
    INPUT_CLASS = 'form-control'
    INPUT_ERROR_CLASS = 'is-invalid'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email address'
        self.fields['username'].widget.attrs.update({'class': self.INPUT_CLASS})
        self.fields['password'].widget.attrs.update({'class': self.INPUT_CLASS})

    def is_valid(self):
        if '__all__' in self.errors.keys():
            for _, field in self.fields.items():
                field.widget.attrs.update({
                    'class': self.INPUT_CLASS + ' ' + self.INPUT_ERROR_CLASS
                })
        return super(CustomAuthenticationForm, self).is_valid()


class CustomUserCreationForm(UserCreationForm):
    INPUT_CLASS = 'form-control'
    INPUT_ERROR_CLASS = 'is-invalid'

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'middle_name',
                  'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': self.INPUT_CLASS
            })

    def is_valid(self):
        if '__all__' in self.errors.keys():
            for _, field in self.fields.items():
                field.widget.attrs.update({
                    'class': self.INPUT_CLASS + ' ' + self.INPUT_ERROR_CLASS
                })

        elif len(self.errors) > 0:
            for item in self.errors.keys():
                field = self.fields.get(item)
                if field:
                    field.widget.attrs.update({
                        'class': self.INPUT_CLASS + ' ' + self.INPUT_ERROR_CLASS
                    })

        return super(CustomUserCreationForm, self).is_valid()
