from django.contrib import admin
from .models import Categoria, Producto, Usuario, DireccionEnvio, Carrito, ElementoCarrito, Orden, ElementoOrden, Historial, Pago, Notificacion, Envase

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(DireccionEnvio)
admin.site.register(Carrito)
admin.site.register(ElementoCarrito)
admin.site.register(Orden)
admin.site.register(ElementoOrden)
admin.site.register(Historial)
admin.site.register(Pago)
admin.site.register(Notificacion)
admin.site.register(Envase)