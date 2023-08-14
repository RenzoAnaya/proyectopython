from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Envase(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre del envase")
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Factor de costo")

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='productos_imagenes', blank=True, null=True)
    envase = models.ForeignKey(Envase, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de envase")

    def __str__(self):
        return self.nombre

    
class DireccionEnvio(models.Model):
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.direccion}, {self.distrito}, {self.ciudad}"
    
    
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.ForeignKey(DireccionEnvio, on_delete=models.SET_NULL, null=True)
    telefono = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.total for item in self.elementocarrito_set.all())
    
class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField()

    @property
    def total(self):
        return self.producto.precio * self.cantidad
    
class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.ForeignKey(DireccionEnvio, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega_deseada = models.DateField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    completado = models.BooleanField(default=False)
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_total_a_pagar(self):
        self.total_a_pagar = self.total + self.costo_envio - self.descuento
        self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.id}"
    
class ElementoOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def total(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"
    
class Historial(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

class Pago(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class Notificacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
