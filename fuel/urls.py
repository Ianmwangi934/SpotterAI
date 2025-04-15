from django.urls import path
from .views import RouteAPIView,FuelMapView,RouteInputeView

urlpatterns = [
    path('api/route/', RouteAPIView.as_view(), name='route-api'),
    path("map/", FuelMapView.as_view(), name='Fuel-map'),
    path("", RouteInputeView.as_view(), name='route-input'),
]