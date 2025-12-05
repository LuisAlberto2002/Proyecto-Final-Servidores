from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions, serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiResponse
)

from django.conf import settings
from django.core.mail import send_mail

from .forms import FacturesForm, CarsForm
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
            descripcion = ''

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
        # Preparar contenido del email
        contenido_email = f"""El servicio ha sido creado exitosamente:

📋 Nombre: {name}
💰 Costo: ${costo}
📝 Descripción: {descripcion if descripcion else 'Sin descripción'}
👤 Creado por: {request.user.username}
📅 Fecha: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}

El nuevo servicio ya está disponible en el sistema."""
        
        email_enviado = enviar_email(
            usuario=request.user,
            asunto=f'✅ Nuevo Servicio Creado: {name}',
            contenido=contenido_email
        )
        
        if email_enviado:
            messages.success(request, f'✅ Servicio "{name}" creado exitosamente. Email de confirmación enviado.')
        else:
            messages.warning(request, f'⚠️ Servicio "{name}" creado, pero no se pudo enviar el email de confirmación.')
        
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
            descripcion = ''

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


def _get_client_for_user(user):
    """Devuelve el cliente asociado al usuario o None."""
    try:
        return Clients.objects.get(user=user)
    except Clients.DoesNotExist:
        return None
    

@login_required
def cars_list(request):
    client = _get_client_for_user(request.user)
    if not client:
        messages.error(request, "No tienes un cliente asociado.")
        cars = Cars.objects.none()
    else:
        cars = Cars.objects.filter(client=client)

    return render(request, "cars/cars_list.html", {"cars": cars})


@login_required
def cars_create(request):
    client = _get_client_for_user(request.user)
    if not client:
        messages.error(request, "No tienes un cliente asociado.")
        return redirect("cars_list")

    if request.method == "POST":
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.client = client          # cliente_id según tu ER
            car.save()
            messages.success(request, "Vehículo creado correctamente.")
            return redirect("cars_list")
    else:
        form = CarsForm()

    return render(request, "cars/cars_form.html", {"form": form, "action": "Crear"})


@login_required
def cars_edit(request, pk):
    client = _get_client_for_user(request.user)
    if not client:
        messages.error(request, "No tienes un cliente asociado.")
        return redirect("cars_list")

    car = get_object_or_404(Cars, pk=pk)

    # Garantizar que el auto pertenece al cliente logueado
    if car.client != client:
        messages.error(request, "No puedes editar este vehículo.")
        return redirect("cars_list")

    if request.method == "POST":
        form = CarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente.")
            return redirect("cars_list")
    else:
        form = CarsForm(instance=car)

    return render(request, "cars/cars_form.html", {"form": form, "action": "Editar"})


@login_required
def cars_delete(request, pk):
    client = _get_client_for_user(request.user)
    if not client:
        messages.error(request, "No tienes un cliente asociado.")
        return redirect("cars_list")

    car = get_object_or_404(Cars, pk=pk)

    if car.client != client:
        messages.error(request, "No puedes eliminar este vehículo.")
        return redirect("cars_list")

    if request.method == "POST":
        car.delete()
        messages.success(request, "Vehículo eliminado correctamente.")
        return redirect("cars_list")

    return render(request, "cars/cars_confirm_delete.html", {"car": car})


def enviar_email(usuario, asunto, contenido):
    """Función para enviar emails"""
    try:
        mensaje = f"""
        Hola {usuario.first_name or usuario.username},

        {contenido}
        
        ---
        ATLAS - Correo Automático, por favor no respondas a este mensaje.
        """
        
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        return False
