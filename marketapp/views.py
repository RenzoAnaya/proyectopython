from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import *

def anonymous_required(function=None, redirect_url='/'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def about(request):
    return render(request,"marketapp/about.html")

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
    usuario = None
    direccion_nueva = None
    ciudad_nueva = None
    distrito_nuevo = None
    codigo_postal_nuevo = None
    
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(username=request.user.username)
            direccion_nueva = usuario.direccion
            ciudad_nueva = usuario.ciudad
            distrito_nuevo = usuario.distrito
            codigo_postal_nuevo = usuario.codigo_postal
        except Usuario.DoesNotExist:
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
            direccion_nueva = form.cleaned_data['direccion_nueva']
            ciudad_nueva = form.cleaned_data['ciudad_nueva']
            distrito_nuevo = form.cleaned_data['distrito_nuevo']
            codigo_postal_nuevo = form.cleaned_data['codigo_postal_nuevo']
            
            orden = form.save(commit=False)
            orden.total = total
            orden.descuento = 0  
            orden.costo_envio = 10 
            orden.total_a_pagar = calcular_total_a_pagar(total, orden.descuento, orden.costo_envio)

            
            if all([direccion_nueva, ciudad_nueva, distrito_nuevo, codigo_postal_nuevo]):
                nueva_direccion_envio = DireccionEnvio.objects.create(
                    direccion=direccion_nueva,
                    ciudad=ciudad_nueva,
                    distrito=distrito_nuevo,
                    codigo_postal=codigo_postal_nuevo,
                )
                orden.direccion = nueva_direccion_envio  # Asignar la dirección creada a la orden
                
            orden.save()
            
            for item in carrito:
                producto = Producto.objects.get(pk=item['producto_id'])
                elemento_orden = ElementoOrden(orden=orden, producto=producto, cantidad=item['cantidad'])
                elemento_orden.save()

            del request.session['carrito']

            return redirect('/confirmacion')  
    else:
        initial_data = {
            'first_name': usuario.first_name if usuario else '',
            'last_name': usuario.last_name if usuario else '',
            'email': usuario.email if usuario else '',
            'telefono': usuario.telefono if usuario else '',
            'costo_envio': 10,
            'descuento': 0,
            'total_a_pagar': calcular_total_a_pagar(total, 0, 10),
        }

        if usuario:
            initial_data['ciudad_nueva'] = usuario.ciudad
            initial_data['distrito_nuevo'] = usuario.distrito
            initial_data['codigo_postal_nuevo'] = usuario.codigo_postal

        form = OrdenForm(initial=initial_data)

    context = {
        'carrito': productos_en_carrito,
        'total': total,
        'form': form
    }
    
    return render(request, 'marketapp/cliente/resumenDeOrden.html', context)


def confirmacion(request):
    return render(request, 'marketapp/cliente/confirmacion.html')



#LOGIN
@anonymous_required()
def login_request(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Obtenemos el usuario autenticado
            login(request, user)
            
            try:
                avatar = Avatar.objects.get(usuario=user).imagen.url
            except Avatar.DoesNotExist:
                avatar = '/media/avatares/default.png'
            
            request.session['avatar'] = avatar
            return render(request, "marketapp/index.html", {"mensaje": f"Bienvenido {user.first_name}"})
        else:
            return render(request, "marketapp/login.html", {"form": form, "mensaje": "Usuario o clave incorrectos"})
    else:
        form = EmailAuthenticationForm()
        return render(request, "marketapp/login.html", {"form": form})

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            form.save()
            return render(request, "marketapp/index.html", {"mensaje":"Usuario creado"})
    else:
        form = RegistroUsuariosForm()
    return render(request, "marketapp/registro.html", {"form":form})


@login_required
def editarPerfil(request):
    usuario = request.user
    avatar_actual = None

    try:
        avatar_actual = Avatar.objects.get(usuario=usuario)
    except Avatar.DoesNotExist:
        pass

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            user = form.save(commit=False)

            # CONTRASEÑA
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 and password2:
                if password1 == password2:
                    user.set_password(password1)
                else:
                    form.add_error(None, "Las contraseñas no coinciden")

            user.save()

            # AVATAR
            avatar_imagen = request.FILES.get('imagen', None)
            if avatar_imagen:  
                if avatar_actual:  
                    avatar_actual.imagen = avatar_imagen
                    avatar_actual.save()
                else:  
                    Avatar.objects.create(usuario=user, imagen=avatar_imagen)
            elif not avatar_actual:  
                default_image_path = Avatar.get_default_image_path()
                Avatar.objects.create(usuario=user, imagen=default_image_path)

            return render(request, "marketapp/index.html", {"mensaje":"Usuario actualizado"})
    else:
        # DATA INICIAL
        initial_data = {
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'email': usuario.email,
            'telefono': usuario.telefono ,
            'direccion': usuario.direccion ,
            'imagen': avatar_actual.imagen.url if avatar_actual else Avatar.get_default_image_path()
        }
        form = UserEditForm(instance=usuario, initial=initial_data)

    return render(request, "marketapp/editarPerfil.html", {'form':form, 'usuario':usuario.username})




#VIEWS ADMIN

#PRODUCTO

def indexAdmin(request):
    return render(request,"marketapp/admin/adminIndex.html")

class ProductoAdminListView(LoginRequiredMixin,ListView):
    model = Producto
    template_name = 'marketapp/admin/producto/list.html'
    context_object_name = 'productos'
    queryset = Producto.objects.all().order_by('categoria')

class ProductoAdminDetailView(LoginRequiredMixin,DetailView):
    model = Producto
    template_name = 'marketapp/admin/producto/detail.html'
    context_object_name = 'producto'

class ProductoAdminCreateView(LoginRequiredMixin,CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'marketapp/admin/producto/create.html'
    success_url = reverse_lazy('administracion:admin_producto_list')

class ProductoAdminUpdateView(LoginRequiredMixin,UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'marketapp/admin/producto/edit.html'
    success_url = reverse_lazy('administracion:admin_producto_list')

class ProductoAdminDeleteView(LoginRequiredMixin,DeleteView):
    model = Producto
    template_name = 'marketapp/admin/producto/delete.html'
    success_url = reverse_lazy('administracion:admin_producto_list')
    
#ORDEN
class OrdenAdminListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'marketapp/admin/orden/list.html'
    context_object_name = 'ordenes'


class OrdenAdminDetailView(LoginRequiredMixin, DetailView):
    model = Orden
    template_name = 'marketapp/admin/orden/detail.html'
    context_object_name = 'orden'

class OrdenAdminCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'marketapp/admin/orden/create.html'
    success_url = reverse_lazy('administracion:admin_orden_list')
    
class OrdenAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'marketapp/admin/orden/edit.html'
    success_url = reverse_lazy('administracion:admin_orden_list')
    
class OrdenAdminDeleteView(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'marketapp/admin/orden/delete.html'
    success_url = reverse_lazy('administracion:admin_orden_list')