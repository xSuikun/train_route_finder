from django.urls import path

from .views import *

urlpatterns = [
    path('', RoutesHome.as_view(), name='home'),
    path('find_routes/', SearchRoutes.as_view(), name='find_routes'),
    path('create_route/', CreateRoute.as_view(), name='create_route'),
    path('save_route/', SaveRoute.as_view(), name='save_route'),
    path('routes_list/', RoutesList.as_view(), name='routes_list'),
    path('<int:pk>/', RouteDetail.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDelete.as_view(), name='delete'),
]
