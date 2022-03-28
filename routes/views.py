from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, CreateRouteForm
from routes.models import Route
from routes.services import get_routes
from trains.models import Train


__all__ = (
    'RoutesHome',
    'SearchRoutes',
    'CreateRoute',
    'SaveRoute',
    'RoutesList',
    'RouteDetail',
    'RouteDelete',
)


class RoutesHome(FormView):
    form_class = RouteForm
    template_name = 'routes/home.html'
    success_url = reverse_lazy('routes:home')


class SearchRoutes(View):
    def get(self, request):
        form = RouteForm()
        messages.warning(request, 'Нет данных для поиска')
        return render(request, 'routes/home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.warning(request, e)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})


class CreateRoute(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        form = CreateRouteForm()
        messages.warning(request, 'Нет данных для маршрута')
        return render(request, 'routes/create_route.html', {'form': form})

    def post(self, request, *args, **kwargs):
        context = {}
        data = request.POST
        travel_time = data['travel_time']
        from_city_id = data['from_city']
        to_city_id = data['to_city']
        trains_ids = data['trains'].split(',')
        trains_ids = [int(t) for t in trains_ids if t.isdigit()]
        trains = Train.objects.filter(id__in=trains_ids).select_related('from_city', 'to_city')
        cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
        form = CreateRouteForm(
            initial={
                'from_city': cities[int(from_city_id)],
                'to_city': cities[int(to_city_id)],
                'travel_time': int(travel_time),
                'trains': trains
            }
        )
        context['form'] = form
        return render(request, 'routes/create_route.html', context)


class SaveRoute(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        messages.warning(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/routes')

    def post(self, request, *args, **kwargs):
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Маршрут успешно сохранен')
            return HttpResponseRedirect('/routes')
        else:
            messages.warning(request, 'Произошла ошибка при сохранении маршрута')
            return HttpResponseRedirect('/routes')
        return render(request, 'routes/create_route.html', {'form': form})


class RoutesList(ListView):
    model = Route
    template_name = 'routes/routes_list.html'
    context_object_name = 'routes'
    paginate_by = 10

    def get_queryset(self):
        return Route.objects.all()


class RouteDetail(DetailView):
    model = Route
    template_name = 'routes/route_detail.html'
    context_object_name = 'route'
    slug_url_kwarg = 'pk'


class RouteDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Route
    context_object_name = 'route'
    success_url = reverse_lazy('routes:home')
    template_name = 'routes/delete_route.html'
    success_message = "Маршрут успешно удален"
    login_url = '/accounts/login'
