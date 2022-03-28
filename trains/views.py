from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView

from trains.forms import TrainForm
from trains.models import Train

__all__ = (
    'TrainsHome',
    'TrainDetail',
    'TrainCreate',
    'TrainUpdate',
    'TrainDelete',
)


class TrainsHome(ListView):
    model = Train
    template_name = 'trains/home.html'
    context_object_name = 'trains'
    extra_context = {'title': 'Поезда'}
    paginate_by = 10

    def get_queryset(self):
        return Train.objects.all()


class MyUpdateView(UpdateView):
    def get_success_url(self):
        if not 'pk' in self.kwargs:
            return reverse_lazy('trains:home')
        return reverse_lazy('trains:update', kwargs={'pk': self.object.pk})


class TrainDetail(DetailView):
    model = Train
    template_name = 'trains/detail.html'
    context_object_name = 'train'
    slug_url_kwarg = 'pk'


class TrainCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    success_url = reverse_lazy('trains:add')
    template_name = 'trains/add_train.html'
    success_message = "Город успешно добавлен"
    login_url = '/accounts/login'


class TrainUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    context_object_name = 'train'
    template_name = 'trains/update_train.html'
    success_message = "Город успешно отредактирован"
    login_url = '/accounts/login'

    def get_success_url(self):
        return reverse_lazy('trains:update', kwargs={'pk': self.object.pk})


class TrainDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Train
    context_object_name = 'train'
    success_url = reverse_lazy('trains:home')
    template_name = 'trains/delete_train.html'
    success_message = "Город успешно удален"
    login_url = '/accounts/login'
