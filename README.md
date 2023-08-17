# proyectopython

ORGANIK

Credenciales:
- Usuario: admin
- Contraseña: Coder2023



Esta aplicación está basada en un supermercado en el que puedes comprar simulando tu lista de compras. Para lograr esto necesitamos productos que cuenten con categorías y envases (o peso). Los Usuarios crean ordenes que incluyen gracias al modelo ElementoOrden los productos que el cliente desea. También generamos un modelo carrito pero dada la rapidez del uso de este, en principio se borra con la creación de la Orden. La orden tiene sus propias clase de calculo para hallar el "subtotal" y el "total" de la orden. Finalmente, como la orden debe ser enviada a una direccion, en este caso la orden usa un FK de DireccionEnvio para crear una dirección y usarla para el envío. Esto permitirá luego que el cliente pueda guardar varias direcciones de envío.

La búsqueda en orden/list.html o /administracion/orden se puede realizar con la barrita y apretando buscar y reiniciando borrando lo escrito y presionando buscar.

En resumen estos son los modelos:

Categoria:
nombre: El nombre de la categoría.
descripcion: Descripción opcional de la categoría.



Envase:
nombre: El nombre del envase.
valor: Un factor de costo asociado al envase.



Producto:
nombre: Nombre del producto.
descripcion: Descripción del producto.
precio: Precio del producto.
stock: Cantidad disponible en inventario.
categoria: Categoría a la que pertenece el producto.
imagen: Imagen representativa del producto.
envase: Tipo de envase asociado al producto.



DireccionEnvio:
direccion: Dirección completa.
ciudad: Ciudad de la dirección.
distrito: Distrito de la dirección.
codigo_postal: Código postal.



Avatar:
imagen: Imagen de avatar del usuario.
usuario: Usuario al que pertenece el avatar.



Carrito:
usuario: Usuario propietario del carrito.
fecha_creacion: Fecha en que se creó el carrito.
fecha_actualizacion: Fecha de la última actualización del carrito.



ElementoCarrito:
carrito: Carrito al que pertenece el elemento.
producto: Producto asociado al elemento del carrito.
cantidad: Cantidad del producto en el carrito.



Orden:
usuario: Usuario que realiza la orden.
first_name: Nombre del usuario.
last_name: Apellido del usuario.
email: Correo electrónico del usuario.
telefono: Teléfono del usuario.
direccion: Dirección de entrega.
fecha_creacion: Fecha en que se creó la orden.
fecha_entrega_deseada: Fecha deseada para la entrega.
total: Costo total de la orden.
descuento: Descuento aplicado.
costo_envio: Costo de envío.
completado: Indicador de si la orden está completada.
total_a_pagar: Monto total a pagar considerando descuentos y envío.



ElementoOrden:
orden: Orden a la que pertenece el elemento.
producto: Producto asociado al elemento de la orden.
cantidad: Cantidad del producto en la orden.



Historial:
orden: Orden asociada al registro histórico.
fecha: Fecha del registro histórico.



Pago:
orden: Orden asociada al pago.
monto: Monto pagado.



Notificacion:
usuario: Usuario al que va dirigida la notificación.
mensaje: Contenido de la notificación.
fecha: Fecha de la notificación.


