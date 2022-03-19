from django import forms

from routes.models import Route
from cities.models import City
from trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',
    }), label='Откуда', queryset=City.objects.all().only('pk', 'name'))
    to_city = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',
    }), label='Куда', queryset=City.objects.all().only('pk', 'name'))
    travel_time = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите желаемое время пути',
    }), label='Время в пути')
    cities = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'form-control js-example-basic-multiple',
    }), label='Через города', queryset=City.objects.all().only('pk', 'name'),
        required=False
    )

    class Meta:
        model = Route
        fields = ['from_city', 'to_city', 'travel_time']


class CreateRouteForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название',
    }))
    from_city = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=City.objects.all().only('pk', 'name'))
    to_city = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=City.objects.all().only('pk', 'name'))
    travel_time = forms.IntegerField(widget=forms.HiddenInput)
    trains = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control d-none'}),
                                            queryset=Train.objects.all().only('pk', 'name'))

    class Meta:
        model = Route
        fields = ['name', 'from_city', 'to_city', 'travel_time', 'trains']

