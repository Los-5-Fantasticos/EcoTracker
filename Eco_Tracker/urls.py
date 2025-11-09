from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
]
#con esto existe el URL, es decir la página
    
    path('registro/', views.crear_usuario, name='registro'), 
    
    # RUTA DE INICIO DE SESIÓN
    path('login/', views.iniciar_sesion, name='login'),
    
    # (Otras rutas...)
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # RUTA DE DESTINO DESPUÉS DEL LOGIN
    path('perfil/', views.ver_perfil, name='perfil'),
]
