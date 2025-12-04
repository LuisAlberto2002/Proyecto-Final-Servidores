from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientsViewSet)
router.register(r'cars', views.CarsViewSet)
router.register(r'servicios', views.ServiciosViewSet)
router.register(r'service-orders', views.ServiceOrdersViewSet)
router.register(r'factures', views.FacturesViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('facturaC/',views.CreateFactura, name='Facturas_template'),
    path('facturasD/<str:sn>/',views.DelFactura,name='Delete_factura'),
    path('facturas/',views.CheckFactura,name='Buscar_factura'),
    path('facturasInfo/<str:sn>/',views.Info_factura,name='Factura_info'),

]
