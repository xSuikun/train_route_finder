from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username=username)
            if not user.exists():
                raise forms.ValidationError(f'Пользователя {username} не существует')
            if not check_password(password, user[0].password):
                raise forms.ValidationError(f'Неверный пароль')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(f'Этот аккаунт неактивен')
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        already_user = User.objects.filter(username=username)
        if already_user.exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

