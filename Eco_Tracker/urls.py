from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


    # Página de Inicio
    path('', views.index, name="index"),
    #con esto existe el URL, es decir la página
    
    # RUTA DE REGISTRO CORREGIDA: Apunta a la función real 'crear_usuario'
    path('registro/', views.registro, name='registro'), 
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    
    # RUTA DE INICIO DE SESIÓN
    path('login/', views.iniciar_sesion, name='login'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    
    # (Otras rutas...)
    #path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    # RUTA DE DESTINO DESPUÉS DEL LOGIN
    path('perfil/', views.ver_perfil, name='perfil'),
    
    # RUTA PARA REGISTRAR UN NUEVO ÍTEM RECICLABLE
    path('grabar_registro/', views.grabar_registro, name='grabar_registro'),
    path('show_registrarItem/', views.show_registrar_item, name='show_registrarItem'),
    
    # MOSTRAR ECORUTAS
    path('historia/', views.listar_ecoruta, name='historia_ecorutas'),
]
