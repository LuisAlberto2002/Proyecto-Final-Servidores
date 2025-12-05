from django.urls import path
from . import views

urlpatterns = [
    path('servicios/', views.servicios_list, name='servicios_list'),
    path('servicios/crear/', views.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/editar/', views.servicio_edit, name='servicio_edit'),
]