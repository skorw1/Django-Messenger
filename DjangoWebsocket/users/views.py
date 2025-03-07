from django.shortcuts import render

# Create your views here.

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register_user.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        # Аутентифицируем пользователя
        user = authenticate(self.request, username=username, password=password)

        # Если пользователь аутентифицирован, авторизуем его
        if user is not None:
            login(self.request, user)

        return response

class AuthenticateUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login_user.html'

    def get_success_url(self):
        return reverse_lazy('main')

class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main-page')