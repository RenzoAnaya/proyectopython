from django import forms
from .models import *
from datetime import date, timedelta, datetime


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio']
        
class OrdenForm(forms.ModelForm):
    direccion_nueva = forms.CharField(required=True, label="Dirección", widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Escribe tu dirección...'}))
    ciudad_nueva = forms.CharField(required=True, max_length=100, label="Ciudad")
    distrito_nuevo = forms.CharField(required=True, max_length=100, label="Distrito")
    codigo_postal_nuevo = forms.CharField(required=False, max_length=10, label="Código Postal")
   
    class Meta:
        model = Orden
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_entrega_deseada']
        
        hoy = datetime.today()
        dias_hasta_domingo = (6 - hoy.weekday()) % 7 or 7
        fecha_domingo = hoy + timedelta(days=dias_hasta_domingo)
        fecha_max = fecha_domingo + timedelta(days=1)
        
        widgets = {
            'nombre': forms.TextInput(attrs={'required': 'required'}),
            'apellido': forms.TextInput(attrs={'required': 'required'}),
            'email': forms.EmailInput(attrs={'required': 'required'}),
            'telefono': forms.TextInput(attrs={'required': 'required'}),
            'direccion': forms.Select(attrs={'required': 'required'}),
            'fecha_entrega_deseada': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': fecha_domingo.strftime('%Y-%m-%d'), 
                    'max': fecha_max.strftime('%Y-%m-%d'), 
                    'class': 'bg-white p-2 rounded border',
                    'value': (hoy + timedelta(days=7)).strftime('%Y-%m-%d'),
                }),
        }