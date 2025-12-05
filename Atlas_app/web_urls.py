from django.urls import path
from . import views

urlpatterns = [
    path('servicios/', views.servicios_list, name='servicios_list'),
    path('servicios/crear/', views.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/editar/', views.servicio_edit, name='servicio_edit'),
    path('facturaC/',views.CreateFactura, name='Facturas_template'),
    path('facturasD/<str:sn>/',views.DelFactura,name='Delete_factura'),
    path('facturas/',views.CheckFactura,name='Buscar_factura'),
    path('facturasInfo/<str:sn>/',views.Info_factura,name='Factura_info'),
    path('clients/<int:pk>/orders/', views.ClientsViewSet.as_view({'get': 'orders'})),
]