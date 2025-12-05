from django.urls import path, include
from rest_framework import routers
from .views import (
    ClientsViewSet, CarsViewSet, ServiciosViewSet,
    ServiceOrdersViewSet, FacturesViewSet
)
from . import views

router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet)
router.register(r'cars', CarsViewSet)
router.register(r'servicios', ServiciosViewSet)
router.register(r'service_orders', ServiceOrdersViewSet)
router.register(r'factures', FacturesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
