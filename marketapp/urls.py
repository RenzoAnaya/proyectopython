from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='inicio'),
    path('productos/', pedidoForm, name='pedidoForm'),
    path('resumen_de_orden/', resumenOrden, name='resumenDeOrden'),
    path('confirmacion/', confirmacion, name='confirmacion'),
]