from django.urls import path

from .views import *

urlpatterns = [
    path('', RoutesHome.as_view(), name='home'),
    path('find_routes/', SearchRoutes.as_view(), name='find_routes'),
    # path('add/', TrainCreate.as_view(), name='add'),
    # path('update/<int:pk>/', TrainUpdate.as_view(), name='update'),
    # path('delete/<int:pk>/', TrainDelete.as_view(), name='delete'),
    # path('<int:pk>/', TrainDetail.as_view(), name='detail'),
]
