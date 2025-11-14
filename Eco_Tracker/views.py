from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login # Herramientas para login
from django.contrib.auth.models import User         # Modelo para crear usuarios
from django.contrib import messages                 # Para mensajes de éxito/error
from django.db import IntegrityError                # Para manejar usuarios/emails duplicados
from django.contrib.auth.decorators import login_required 
from .forms import CarUsageForm
from .models import Registro, Item, Clientes

def index(request):
    """Renderiza la página de inicio."""
    return render(request, "ecotracker/index.html")
    #Renderizar los hmtl, es decir que se vea la página xd 

# --- FUNCIÓN 1: CREAR USUARIO (REGISTRO) ---
def crear_usuario(request):
    """Maneja el envío del formulario de registro, crea el usuario y redirige al login."""
    
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        nombre = request.POST.get('nombre')
        username = request.POST.get('username')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        telefono = request.POST.get('telefono')

        # 2. Validación básica
        if not (username and correo and password):
            messages.error(request, "Todos los campos obligatorios deben ser llenados.")
            return render(request, "ecotracker/index.html")

        # 3. Creación del usuario segura
        try:
            # Crea un nuevo objeto User y hashea la contraseña
            user = User.objects.create_user(
                username=username,
                email=correo,
                password=password
            )
            
            # Guarda el nombre completo
            user.first_name = nombre
            user.save() 

            messages.success(request, '🎉 ¡Cuenta creada exitosamente! Por favor, inicia sesión.')
            
            # Redirige a la página de inicio de sesión
            return redirect('login') 

        except IntegrityError:
            # Error si el username o email ya existen
            messages.error(request, 'El nombre de usuario o correo electrónico ya está registrado.')
            return render(request, "ecotracker/index.html")
        
        except Exception:
            messages.error(request, 'Ocurrió un error inesperado al registrarte.')
            return render(request, "ecotracker/index.html")

    # Si la solicitud es GET, simplemente renderiza el formulario de registro
    return render(request, "ecotracker/index.html")


# --- FUNCIÓN 2: INICIAR SESIÓN (LOGIN) ---
def iniciar_sesion(request):
    """Maneja la autenticación del usuario."""
    
    if request.method == 'POST':
        username_o_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # 1. Autenticar: Verifica credenciales
        user = authenticate(request, username=username_o_email, password=password)
        
        if user is not None:
            # 2. Login: Crea la sesión del usuario
            login(request, user)
            
            messages.success(request, f'¡Bienvenido, {user.username}!')
            
            # Redirige a la página de perfil/datos (Asegúrate de que 'perfil' exista en urls.py)
            return redirect('perfil') 
        else:
            # 3. Error
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return render(request, 'ecotracker/login.html')
            
    # Si es GET, muestra la página de login
    return render(request, 'ecotracker/login.html')


# --- FUNCIÓN 3: VER PERFIL (PÁGINA DE DATOS PROTEGIDA) ---
@login_required(login_url='login') 
def ver_perfil(request):
    """Renderiza la página del perfil con los datos y estadísticas (Protegida)."""
    
    context = {
        'usuario': request.user,
        # Aquí irán los datos reales para las estadísticas
    }
    
    return render(request, 'ecotracker/perfil.html', context)

@login_required(login_url='login')
def registrar_auto(request):
    """Registra el uso del auto y calcula la huella de carbono."""
    
    if request.method == 'POST':
        form = CarUsageForm(request.POST)
        if form.is_valid():
            manejó_auto = form.cleaned_data['manejó_auto']
            
            if manejó_auto == 'yes':
                distancia = form.cleaned_data.get('distancia', 0)
                # Factor simple: 0.21 kg CO2 por km (promedio de autos)
                huella = distancia * 0.21
                
                messages.success(request, f'✅ Huella de carbono: {huella:.2f} kg CO2')
                return render(request, 'ecotracker/input_data.html', {'form': form, 'huella': huella})
            else:
                messages.info(request, 'No registraste uso de auto.')
                return render(request, 'ecotracker/input_data.html', {'form': form})
    else:
        form = CarUsageForm()
    
    return render(request, 'ecotracker/input_data.html', {'form': form})
    
def calcular_api(request):
    """API simple para calcular huella de carbono basada en distancia recorrida en auto."""
    from django.http import JsonResponse

    distancia = float(request.GET.get('distancia', 0))
    huella = distancia * 0.21  # Factor simple: 0.21 kg CO2 por km

    return JsonResponse({'distancia': distancia, 'huella_co2_kg': huella})