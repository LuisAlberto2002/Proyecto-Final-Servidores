from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions, serializers
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

from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiResponse
)


from .models import Clients, Cars, Servicios, Service_orders, Factures
from .serializers import (
    ClientsSerializer, CarsSerializer, ServiciosSerializer,
    ServiceOrdersSerializer, FacturesSerializer
)

# Client viewset :)
@extend_schema_view(
    list=extend_schema(
        summary="Listar clientes",
        description="Listado general de clientes del sistema."
    ),
    retrieve=extend_schema(
        summary="Detalle de cliente",
        description="Obtener información de un cliente específico."
    ),
    create=extend_schema(
        summary="Crear cliente (US01)",
        description="Registrar un nuevo cliente validando correo único."
    ),
    update=extend_schema(
        summary="Actualizar cliente (US03)",
        description="Editar datos de un cliente con validación de correo único."
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente cliente",
        description="Actualización parcial usando PATCH."
    ),
    destroy=extend_schema(
        summary="Eliminar cliente (US04)",
        description="Elimina un cliente y devuelve mensaje de confirmación."
    )
)
class ClientsViewSet(viewsets.ModelViewSet):
    """CRUD para Clientes"""
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'email']
    ordering = ['name']

    # --- US01 y US03: Validar correo duplicado ---
    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        if Clients.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Este correo ya está registrado."})
        serializer.save()

    def perform_update(self, serializer):
        email = serializer.validated_data.get("email")
        obj_id = self.get_object().id
        if Clients.objects.filter(email=email).exclude(id=obj_id).exists():
            raise serializers.ValidationError({"email": "Este correo ya está registrado."})
        serializer.save()

    # --- US02: Endpoint para consultar órdenes del cliente ---
    @extend_schema(
        summary="Consultar órdenes del cliente (US02)",
        description="Lista todas las órdenes asociadas a un cliente.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID del cliente",
                required=True,
                type=int
            )
        ],
        responses={200: OpenApiResponse(description="Órdenes encontradas")}
    )
    @action(detail=True, methods=["get"], url_path="orders")
    def get_client_orders(self, request, pk=None):
        client = self.get_object()
        orders = Service_orders.objects.filter(Client=client)

        data = [
            {
                "order_id": o.id,
                "code": o.code,
                "car_matricula": o.car.matricula,
                "servicio": o.servicio.name,
                "costo": o.servicio.costo,
                "emision_date": o.emision_date,
                "delivery_Date": o.delivery_Date,
            }
            for o in orders
        ]

        return Response({"client": client.name, "orders": data})

    # --- US04: Mensaje personalizado al eliminar ---
    def destroy(self, request, *args, **kwargs):
        client = self.get_object()
        super().destroy(request, *args, **kwargs)
        return Response({"message": f"Cliente '{client.name}' eliminado correctamente."})

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

#Crear la factura en base a un formulario

def CreateFactura(request):
    facturas = Factures.objects.create()

#Eliminar la factura a partir de su code

def DelFactura(request):
    factura = Factures.objects.delete(code = request.code)
