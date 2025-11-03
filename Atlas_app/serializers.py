from rest_framework import serializers
from .models import Clients, Cars, Servicios, Service_orders, Factures


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'


class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = '__all__'


class ServiceOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_orders
        fields = '__all__'


class FacturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factures
        fields = '__all__'
