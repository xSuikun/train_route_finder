from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cities.models import City
from cities.forms import CityForm

__all__ = (
    'CitiesHome',
    'CityDetail',
    'CityCreate',
    'CityUpdate',
    'CityDelete',
)


class MyUpdateView(UpdateView):
    def get_success_url(self):
        if not 'pk' in self.kwargs:
            return reverse_lazy('cities:home')
        return reverse_lazy('cities:update', kwargs={'pk': self.object.pk})


class CitiesHome(ListView):
    model = City
    template_name = 'cities/home.html'
    context_object_name = 'cities'
    extra_context = {'title': 'Города'}
    paginate_by = 10

    def get_queryset(self):
        return City.objects.all().order_by('id')


class CityDetail(DetailView):
    model = City
    template_name = 'cities/detail.html'
    context_object_name = 'city'
    slug_url_kwarg = 'pk'


class CityCreate(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    success_url = reverse_lazy('cities:add')
    template_name = 'cities/add_city.html'
    success_message = "Город успешно добавлен"


class CityUpdate(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    context_object_name = 'city'
    template_name = 'cities/update_city.html'
    success_message = "Город успешно отредактирован"

    def get_success_url(self):
        return reverse_lazy('cities:update', kwargs={'pk': self.object.pk})


class CityDelete(SuccessMessageMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:home')
    template_name = 'cities/delete_city.html'
    success_message = "Город успешно удален"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

