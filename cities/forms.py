from django import forms

from cities.models import City


class CityForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название',
    }), label='Название')

    class Meta:
        model = City
        fields = ['name']
