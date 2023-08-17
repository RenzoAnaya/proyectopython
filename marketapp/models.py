from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Envase(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre del envase")
    valor = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Factor de costo"
    )

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to="productos_imagenes", blank=True, null=True)
    envase = models.ForeignKey(
        Envase, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de envase"
    )

    def __str__(self):
        return self.nombre


class DireccionEnvio(models.Model):
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.direccion}, {self.distrito}, {self.ciudad}"


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    distrito = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='correo electrónico')

    CLIENTE = "cliente"
    ADMINISTRADOR = "administrador"
    TIPO_USUARIO_CHOICES = [
        (CLIENTE, "Cliente"),
        (ADMINISTRADOR, "Administrador"),
    ]

    tipo_usuario = models.CharField(
        max_length=15,
        choices=TIPO_USUARIO_CHOICES,
        default=CLIENTE,
    )

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    usuario = models.ForeignKey("marketapp.Usuario", on_delete=models.CASCADE)

    @classmethod
    def get_default_image_path(cls):
        return 'avatares/default.png'


class Carrito(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, null=True, blank=True
    )
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
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
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
    
    def recalcular_total(self):
        total = 0
        elementos = self.elementoorden_set.all()
        for elemento in elementos:
            total += elemento.total
        self.total = total

    def save(self, recalculate_elements=True, *args, **kwargs):
        super(Orden, self).save(*args, **kwargs)
        
        if recalculate_elements:
            self.recalcular_total()
            self.calcular_total_a_pagar()
            super(Orden, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.id}"


class ElementoOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def total(self):
        return self.producto.precio * self.cantidad
    
    def save(self, recalculate_order=True, *args, **kwargs):
        super(ElementoOrden, self).save(*args, **kwargs)
        if recalculate_order:
            self.orden.recalcular_total()
            self.orden.calcular_total_a_pagar()
            self.orden.save(recalculate_elements=False)
            
    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"


class Historial(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)


class Pago(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)


class Notificacion(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True, blank=True
    )
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
