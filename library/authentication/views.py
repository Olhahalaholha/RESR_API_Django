"""
Views for authentication
"""
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer


def registration(request):
    """User registration view"""
    if request.method == 'GET':
        registration_form = CustomUserCreationForm()
        return render(request, 'authentication/registration.html', {
            'registration_form': registration_form
        })
    if request.method == 'POST':
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = CustomUser.objects.get(
                email=registration_form.cleaned_data['email']
            )
            login(request, user)
            return redirect('authentication:registration_success')
        else:
            res = {
                'registration_form': registration_form,
            }
            return render(request, 'authentication/registration.html', res)


@login_required
def registration_success(request):
    """Success registration view"""
    text = 'Congratulations! You have successfully registered.'
    return render(request, 'authentication/success-registration.html', {'text': text})


def login_view(request):
    """User login view"""
    if request.user and request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'GET':
        login_form = CustomAuthenticationForm()
        return render(request, 'authentication/login.html', {'login_form': login_form})

    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('core:index')

        return render(request, 'authentication/login.html',{'login_form': login_form})


@login_required
def logout_view(request):
    """User logout view"""
    if request.method == 'POST':
        logout(request)
        return redirect('authentication:login')
    else:
        raise Http404


class UserAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserDetailsAPIView(APIView):
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk, is_superuser=False)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.update(user, request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
