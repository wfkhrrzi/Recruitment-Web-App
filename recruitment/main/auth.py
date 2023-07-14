from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import logout


from .models import Users

class CustomLoginRequired(LoginRequiredMixin):
    pass
    # def handle_no_permission(self) -> HttpResponseForbidden:
    #     return HttpResponseForbidden("You do not have access to this page")

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def logout(request):
    return logout_then_login(request,login_url=reverse_lazy('main:login'))

class CustomLoginView(LoginView):
    template_name = 'admin/login.html'
    next_page = reverse_lazy('main:index')
    success_url = reverse_lazy('main:index')
    redirect_authenticated_user = True
