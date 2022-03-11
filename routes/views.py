from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from routes.forms import RouteForm
from routes.services import get_routes


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

