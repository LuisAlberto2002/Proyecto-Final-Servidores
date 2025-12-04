from .models import Factures, Servicios
from django import forms

#Fomulario para llenar una 

class FacturesForm(forms.ModelForm):
    monto = forms.FloatField()
    class Meta:
        model = Factures
        fields= ['monto']

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['name', 'costo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo'})
        }