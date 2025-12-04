from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FacturesForm
from django.http import JsonResponse
import json


from .models import Clients, Cars, Servicios, Service_orders, Factures
from .serializers import (
    ClientsSerializer, CarsSerializer, ServiciosSerializer,
    ServiceOrdersSerializer, FacturesSerializer
)


class ClientsViewSet(viewsets.ModelViewSet):
    """CRUD para Clientes"""
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'email']
    ordering = ['name']


class CarsViewSet(viewsets.ModelViewSet):
    """CRUD para Autos"""
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'color', 'model']
    search_fields = ['matricula']
    ordering_fields = ['model', 'matricula']
    ordering = ['model']


class ServiciosViewSet(viewsets.ModelViewSet):
    """CRUD para Servicios"""
    queryset = Servicios.objects.all()
    serializer_class = ServiciosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'Description']
    ordering_fields = ['name', 'costo']
    ordering = ['name']


class ServiceOrdersViewSet(viewsets.ModelViewSet):
    """Órdenes de servicio"""
    queryset = Service_orders.objects.all()
    serializer_class = ServiceOrdersSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Client', 'car', 'servicio']
    search_fields = ['code', 'Client__name', 'car__matricula']
    ordering_fields = ['emision_date', 'delivery_Date']
    ordering = ['-emision_date']


class FacturesViewSet(viewsets.ModelViewSet):
    """Facturas"""
    queryset = Factures.objects.all()
    serializer_class = FacturesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'servicio', 'service_order']
    search_fields = ['client__name']
    ordering_fields = ['fecha', 'monto']
    ordering = ['-fecha']


#Devolver la informacion de la factura a partir de su code.

def CheckFactura(request,code):
    facturas = Factures.objects.get(code = code)

#Crear la factura en base a un formulario

def CreateFactura(request):
    facturas = Factures.objects.create()
    


#Eliminar la factura a partir de su code
    
def DelFactura(request):
    factura = Factures.objects.delete(code = request.code)

def servicios_list(request):
    """SV02 - Consulta de servicios"""
    servicios = Servicios.objects.all()
    search = request.GET.get('search', '')
    
    if search:
        servicios = servicios.filter(name__icontains=search)
    
    context = {
        'servicios': servicios,
        'search': search,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'servicios/servicios_list.html', context)


@login_required
def servicio_create(request):
    """SV01 - Alta de servicio (solo Administrador)"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('servicios_list')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        costo = request.POST.get('costo', '').strip()
        
        # Validación
        if not name:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Crear'})
        
        if not descripcion:
            descripcion = '---'

        if not costo:
            messages.error(request, 'El costo es obligatorio.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Crear'})
        
        try:
            costo = float(costo)
            if costo < 0:
                raise ValueError("El costo debe ser positivo")
        except ValueError:
            messages.error(request, 'El costo debe ser un número válido y positivo.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Crear'})
        
        if Servicios.objects.filter(name=name).exists():
            messages.error(request, 'Ya existe un servicio con ese nombre.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Crear'})
        
        Servicios.objects.create(name=name, Description=descripcion, costo=costo)
        messages.success(request, f'Servicio "{name}" creado exitosamente.')
        return redirect('servicios_list')
    
    return render(request, 'servicios/servicio_form.html', {'action': 'Crear'})


@login_required
def servicio_edit(request, pk):
    """SV03 - Edición de servicio (solo Administrador)"""
    servicio = get_object_or_404(Servicios, pk=pk)
    
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('servicios_list')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        costo = request.POST.get('costo', '').strip()
        
        # Validación
        if not name:
            messages.error(request, 'El nombre del servicio es obligatorio.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Editar', 'servicio': servicio})
        
        if not descripcion:
            descripcion = '---'

        if not costo:
            messages.error(request, 'El costo es obligatorio.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Editar', 'servicio': servicio})
        
        try:
            costo = float(costo)
            if costo < 0:
                raise ValueError("El costo debe ser positivo")
        except ValueError:
            messages.error(request, 'El costo debe ser un número válido y positivo.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Editar', 'servicio': servicio})
        
        # Verificar si el nombre está usado por otro servicio
        if Servicios.objects.filter(name=name).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe otro servicio con ese nombre.')
            return render(request, 'servicios/servicio_form.html', {'action': 'Editar', 'servicio': servicio})
        
        servicio.name = name
        servicio.Description = descripcion
        servicio.costo = costo
        servicio.save()
        messages.success(request, f'Servicio "{name}" actualizado exitosamente.')
        return redirect('servicios_list')
    
    context = {'servicio': servicio, 'action': 'Editar'}
    return render(request, 'servicios/servicio_form.html', context)