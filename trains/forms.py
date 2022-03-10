from django import forms

from cities.models import City
from trains.models import Train


class TrainForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название поезда',
    }), label='Название')
    from_city = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), label='Откуда', queryset=City.objects.all().only('pk', 'name'))
    to_city = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
    }), label='Куда', queryset=City.objects.all().only('pk', 'name'))
    travel_time = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Время в пути',
    }), label='Введите время, требуемое для прохождения маршрута')

    class Meta:
        model = Train
        fields = ['name', 'from_city', 'to_city', 'travel_time']
