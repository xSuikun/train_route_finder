from django import forms

from cities.models import City


class AddCityForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название',
    }), label='Название')

    class Meta:
        model = City
        fields = ['name']


class UpdateCityForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Новое название',
    }), label='Название')

    class Meta:
        model = City
        fields = ['name']
