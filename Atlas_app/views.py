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


class ServiciosViewSet(viewsets.ReadOnlyModelViewSet):
    """Servicios (solo lectura)"""
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
    return render(request,'facturas/factura.html',{'facturas':facturas})

#Crear la factura en base a un formulario

def CreateFactura(request):
    orders = Service_orders.objects.all()
    return render(request,'facturas/factura.html',{'ordenes':orders})
    


#Eliminar la factura a partir de su code
    
def DelFactura(request):
    factura = Factures.objects.delete(code = request.code)
    return render(request,'facturas/factura.html')