from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404


def index(request):
    return render(request,"marketapp/index.html")

@never_cache
def pedidoForm(request):
    categorias = Categoria.objects.all()
    selecciones = request.session.get('selecciones', {})
    
    if request.method == "POST":
        carrito = []
        for producto in Producto.objects.all():
            cantidad_key = f"cantidad_{producto.id}"
            if cantidad_key in request.POST:
                cantidad = request.POST[cantidad_key]
                if int(cantidad) > 0:
                    carrito.append({
                        "producto_id":producto.id,
                        "nombre": producto.nombre,
                        "cantidad": cantidad,
                        "envase": producto.envase.nombre,
                        "precio": str(producto.precio),
                    })

        # Guardar el carrito en la sesión
        request.session['carrito'] = carrito
        return redirect(reverse('resumenDeOrden'))
    
    return render(request, 'marketapp/cliente/productos.html', {'categorias': categorias, 'selecciones':selecciones})

def calcular_total_a_pagar(total, descuento, costo_envio):
    return total - descuento + costo_envio

def resumenOrden(request):
    cliente = None
    direccion_nueva = None
    ciudad_nueva = None
    distrito_nuevo = None
    codigo_postal_nuevo = None
    
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(user=request.user)
            direccion_nueva = cliente.direccion.direccion if cliente.direccion else None
            ciudad_nueva = cliente.direccion.ciudad if cliente.direccion else None
            distrito_nuevo = cliente.direccion.distrito if cliente.direccion else None
            codigo_postal_nuevo = cliente.direccion.codigo_postal if cliente.direccion else None
        except Cliente.DoesNotExist:
            pass
        
    carrito = request.session.get('carrito', [])
    total = 0
    productos_en_carrito = []
    
    for item in carrito:
        try:
            producto = Producto.objects.get(pk=item['producto_id'])  
            item_total = producto.precio * int(item['cantidad'])  
            total += item_total

            productos_en_carrito.append({
                'imagen': producto.imagen,
                'nombre': producto.nombre,
                'cantidad': item['cantidad'],
                'envase': producto.envase.nombre,
                'precio': item_total,  
            })

        except Producto.DoesNotExist:
            pass

    if request.method == "POST":
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.total = total
            #POR AHORA NO ESTOY INCLUYENDO LA LOGICA
            #DE DESCUENTO PARA EL TRABAJO
            orden.descuento = 0  
            orden.costo_envio = 10 
            orden.total_a_pagar = calcular_total_a_pagar(total, orden.descuento, orden.costo_envio)
        
            if all([direccion_nueva, ciudad_nueva, distrito_nuevo, codigo_postal_nuevo]):
                direccion = DireccionEnvio.objects.create(
                    cliente=cliente,
                    direccion=direccion_nueva,
                    ciudad=ciudad_nueva,
                    distrito=distrito_nuevo,
                    codigo_postal=codigo_postal_nuevo,
                )
                orden.direccion_envio = direccion
            orden.save()
            
            for item in carrito:
                producto = Producto.objects.get(pk=item['producto_id'])
                elemento_orden = ElementoOrden(orden=orden, producto=producto, cantidad=item['cantidad'])
                elemento_orden.save()

            del request.session['carrito']

            return redirect('/confimacion')  
    else:
        initial_data = {
            'nombre': cliente.user.first_name if cliente else '',
            'apellido': cliente.user.last_name if cliente else '',
            'email': cliente.user.email if cliente else '',
            'telefono': cliente.telefono if cliente else '',
            'costo_envio': 10,
            'descuento': 0,
            'total_a_pagar': calcular_total_a_pagar(total, 0, 10),
        }

        if cliente and cliente.direccion:
            initial_data['direccion_nueva'] = cliente.direccion.direccion
            initial_data['ciudad_nueva'] = cliente.direccion.ciudad
            initial_data['distrito_nuevo'] = cliente.direccion.distrito
            initial_data['codigo_postal_nuevo'] = cliente.direccion.codigo_postal

        form = OrdenForm(initial=initial_data)

    context = {
        'carrito': productos_en_carrito,
        'total': total,
        'form': form
    }
    
    return render(request, 'marketapp/cliente/resumenDeOrden.html', context)

def confirmacion(request):
    return render(request, 'marketapp/cliente/confirmacion.html')