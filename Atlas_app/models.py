from django.db import models

# Create your models here.

class Clients(models.Model):
    name = models.CharField(max_length=30,default='test')
    phone = models.CharField(max_length=15,default='00 00 00 00 00')
    email = models.EmailField(blank=False,null=False)
    
    def __str__(self):
        return self.name


class Cars(models.Model):
    client = models.ForeignKey(Clients,on_delete=models.CASCADE)
    model = models.CharField(max_length=30, default="Unknown")
    matricula = models.CharField(max_length=7, default="00-000-00")
    color = models.CharField(max_length=30,default="None")
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    def __str__(self):
        return self.matricula

class Servicios(models.Model):
    name = models.CharField(max_length=30)
    Description = models.CharField(max_length=60)
    costo = models.FloatField(default=0.0)
    def __str__(self):
        return self.name



class Service_orders(models.Model):
    Client = models.ForeignKey(Clients,on_delete=models.CASCADE)
    code = models.CharField(max_length=7)
    car = models.ForeignKey(Cars,on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicios,on_delete=models.CASCADE)
    emision_date = models.DateField(auto_now_add=False)
    delivery_Date = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.code

class Factures(models.Model):
    client = models.ForeignKey(Clients,on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicios,on_delete=models.CASCADE)
    service_order= models.ForeignKey(Service_orders,on_delete=models.CASCADE)
    monto = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)
    def __srt__(self):
        return self.code