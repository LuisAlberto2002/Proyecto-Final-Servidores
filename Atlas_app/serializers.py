from rest_framework import serializers
from .models import Clients, Cars, Servicios, Service_orders, Factures


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id', 'name', 'phone', 'email']
        read_only_fields = ['id']


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ['id', 'client', 'model', 'matricula', 'color']
        read_only_fields = ['id']


class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = ['id', 'name', 'Description', 'costo']
        read_only_fields = ['id']


class ServiceOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_orders
        fields = [
            'id', 'Client', 'code', 'car', 'servicio',
            'emision_date', 'delivery_Date'
        ]
        read_only_fields = ['id']


class FacturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factures
        fields = ['id', 'client', 'servicio', 'service_order', 'monto', 'fecha']
        read_only_fields = ['id', 'fecha']
