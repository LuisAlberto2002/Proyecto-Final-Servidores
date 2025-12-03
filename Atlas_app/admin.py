from django.contrib import admin
from .models import Factures, Service_orders,Cars,Clients,Servicios

# Register your models here.

admin.site.register(Factures)
admin.site.register(Cars)
admin.site.register(Service_orders)
admin.site.register(Clients)
admin.site.register(Servicios)
