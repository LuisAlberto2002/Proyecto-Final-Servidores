from django.urls import path, include
from rest_framework import routers
from .views import (
    ClientsViewSet, CarsViewSet, ServiciosViewSet,
    ServiceOrdersViewSet, FacturesViewSet
)
import views

router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet)
router.register(r'cars', CarsViewSet)
router.register(r'servicios', ServiciosViewSet)
router.register(r'service_orders', ServiceOrdersViewSet)
router.register(r'factures', FacturesViewSet)

urlpatterns = [
    path('clients/<int:pk>/orders/', ClientsViewSet.as_view({'get': 'orders'})),
    path('', include(router.urls)),
    path('facturaC/',views.CreateFactura, name='Facturas_template'),
    path('facturasD/<str:sn>/',views.DelFactura,name='Delete_factura'),
    path('facturas/',views.CheckFactura,name='Buscar_factura'),
    path('facturasInfo/<str:sn>/',views.Info_factura,name='Factura_info'),

]
