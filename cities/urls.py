from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', CitiesHome.as_view(), name='home'),
    path('add/', CityCreate.as_view(), name='add'),
    path('update/<int:pk>/', CityUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', CityDelete.as_view(), name='delete'),
    path('<int:pk>/', CityDetail.as_view(), name='detail'),
]
