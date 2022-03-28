from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.forms import UserLoginForm, UserRegistrationForm


__all__ = (
    'LoginView',
    'LogoutView',
    'RegistrationView',
)


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        next_page = request.GET.get('next')
        cache.set('next_page', next_page)
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            next_page = cache.get('next_page') or reverse('routes:home')
            cache.delete('next_page')
            return HttpResponseRedirect(next_page)
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('routes:home'))


class RegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/registration_done.html', {'username': new_user.username})
        else:
            return render(request, 'accounts/registration.html', {'form': form})
