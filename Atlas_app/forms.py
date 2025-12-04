from .models import Factures
from django import forms

#Fomulario para llenar una 

class FacturesForm(forms.ModelForm):
    monto = forms.FloatField()
    class Meta:
        model = Factures
        fields= ['monto']