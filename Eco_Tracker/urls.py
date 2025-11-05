from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


    # Página de Inicio
    path('', views.index, name="index"),
    #con esto existe el URL, es decir la página
    
    # RUTA DE REGISTRO CORREGIDA: Apunta a la función real 'crear_usuario'
    path('registro/', views.crear_usuario, name='registro'), 
    
    # RUTA DE INICIO DE SESIÓN
    path('login/', views.iniciar_sesion, name='login'),
    
    # (Otras rutas...)
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # RUTA DE DESTINO DESPUÉS DEL LOGIN
    path('perfil/', views.ver_perfil, name='perfil'),
]
