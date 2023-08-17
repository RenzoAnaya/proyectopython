from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='inicio'),
    path('about/', about, name='about'),
    
    #PEDIDOS
    path('productos/', pedidoForm, name='pedidoForm'),
    path('resumen_de_orden/', resumenOrden, name='resumenDeOrden'),
    path('confirmacion/', confirmacion, name='confirmacion'),
   
    
    #LOGIN
    path('login/', login_request, name="login"),
    path('logout/', LogoutView.as_view(template_name="marketapp/logout.html"), name="logout"),
    path('registro/', registro, name="registro"),
    path('editar_perfil/', editarPerfil, name="editar_perfil"),
    
    ]
    
    #ADMINISTRADOR
admin_patterns = [
    path('', indexAdmin, name='adminIndex'),
    #PRODUCTO
    path('producto/', ProductoAdminListView.as_view(), name='admin_producto_list'),
    path('producto/<int:pk>/', ProductoAdminDetailView.as_view(), name='admin_producto_detail'),
    path('producto/crear/', ProductoAdminCreateView.as_view(), name='admin_producto_create'),
    path('producto/editar/<int:pk>/', ProductoAdminUpdateView.as_view(), name='admin_producto_edit'),
    path('producto/eliminar/<int:pk>/', ProductoAdminDeleteView.as_view(), name='admin_producto_delete'),
    
    #ORDEN
    path('orden/', OrdenAdminListView.as_view(), name='admin_orden_list'),
    path('orden/<int:pk>/', OrdenAdminDetailView.as_view(), name='admin_orden_detail'),
    path('orden/crear/', OrdenAdminCreateView.as_view(), name='admin_orden_create'),
    path('orden/editar/<int:pk>/', OrdenAdminUpdateView.as_view(), name='admin_orden_edit'),
    path('orden/eliminar/<int:pk>/', OrdenAdminDeleteView.as_view(), name='admin_orden_delete'),
    
    path('usuario/', UsuarioAdminListView.as_view(), name='admin_usuario_list'),
    path('usuario/<int:pk>/', UsuarioAdminDetailView.as_view(), name='admin_usuario_detail'),
    path('usuario/crear/', UsuarioAdminCreateView.as_view(), name='admin_usuario_create'),
    path('usuario/editar/<int:pk>/', UsuarioAdminUpdateView.as_view(), name='admin_usuario_edit'),
    path('usuario/eliminar/<int:pk>/', UsuarioAdminDeleteView.as_view(), name='admin_usuario_delete'),
    
    #ENVASE
    path('envase/', EnvaseAdminListView.as_view(), name='admin_envase_list'),
    path('envase/<int:pk>/', EnvaseAdminDetailView.as_view(), name='admin_envase_detail'),
    path('envase/crear/', EnvaseAdminCreateView.as_view(), name='admin_envase_create'),
    path('envase/editar/<int:pk>/', EnvaseAdminUpdateView.as_view(), name='admin_envase_edit'),
    path('envase/eliminar/<int:pk>/', EnvaseAdminDeleteView.as_view(), name='admin_envase_delete'),
    
    path('categoria/', CategoriaAdminListView.as_view(), name='admin_categoria_list'),
    path('categoria/<int:pk>/', CategoriaAdminDetailView.as_view(), name='admin_categoria_detail'),
    path('categoria/crear/', CategoriaAdminCreateView.as_view(), name='admin_categoria_create'),
    path('categoria/editar/<int:pk>/', CategoriaAdminUpdateView.as_view(), name='admin_categoria_edit'),
    path('categoria/eliminar/<int:pk>/', CategoriaAdminDeleteView.as_view(), name='admin_categoria_delete'),

    
    ]   

urlpatterns += [
    path('administracion/', include((admin_patterns, 'administracion'))),
    ]
    
    
    
