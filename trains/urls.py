from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', TrainsHome.as_view(), name='home'),
    path('add/', TrainCreate.as_view(), name='add'),
    path('update/<int:pk>/', TrainUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDelete.as_view(), name='delete'),
    path('<int:pk>/', TrainDetail.as_view(), name='detail'),
]
