from django.utils import timezone
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout # Herramientas para login
from django.contrib.auth.models import User         # Modelo para crear usuarios
from django.contrib import messages                 # Para mensajes de éxito/error
from django.db import IntegrityError                # Para manejar usuarios/emails duplicados
from django.contrib.auth.decorators import login_required

from Eco_Tracker.models import Item, Registro, Clientes

def index(request):
    """Renderiza la página de inicio."""
    return render(request, "ecotracker/index.html")
    #Renderizar los hmtl, es decir que se vea la página xd 

def registro(request):
    """Renderiza la página de registro."""
    return render(request, "ecotracker/registro.html")

# --- FUNCIÓN 1: CREAR USUARIO (REGISTRO) ---
def crear_usuario(request):
    """Maneja el envío del formulario de registro, crea el usuario y redirige al login."""
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        nombre = request.POST.get('nombre')
        username = request.POST.get('username')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        first_name = request.POST.get('nombre')
        last_name = request.POST.get('apellido')

        # 2. Validación básica
        if not (username and correo and password):
            messages.error(request, "Todos los campos obligatorios deben ser llenados.")
            return render(request, "ecotracker/index.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('registro') # Recarga la página de registro

        # 3. Creación del usuario segura
        try:
            # Crea un nuevo objeto User y hashea la contraseña
            user = User.objects.create_user(
                username=username,
                email=correo,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,
                is_superuser=False
            )
            
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


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('index') # Redirige a la landing page

# --- FUNCIÓN 3: VER PERFIL (PÁGINA DE DATOS PROTEGIDA) ---
@login_required(login_url='login') 
def ver_perfil(request):
    """Renderiza la página del perfil con los datos y estadísticas (Protegida)."""
    todos_los_items = Item.objects.all()
    context = {
        'items': todos_los_items,
        'usuario': request.user,
        # Aquí irán los datos reales para las estadísticas
    }
    
    return render(request, 'ecotracker/perfil.html', context)

@login_required(login_url='login') 
def show_registrar_item(request):
    """Renderiza la página para registrar un nuevo ítem reciclable."""
    todos_los_items = Item.objects.all()
    context = {
        'items': todos_los_items
    }
    
    return render(request, "ecotracker/registrar_item.html", context)

@login_required(login_url='login') 
def grabar_registro(request):
    if request.method == 'POST':
        # Botón pulsado
        action = request.POST.get('action')  # save_return o save_add

        # Campos del formulario (ojo con los names)
        item_id          = request.POST.get('item_id')
        time_sec         = request.POST.get('time_sec') or 0
        distance_km      = request.POST.get('distance_km') or 0
        huella_distancia = request.POST.get('huella_distancia') or 0
        huella_tiempo    = request.POST.get('huella_tiempo') or 0


        # Conversión a tipos numéricos seguros
        try:
            time_sec = int(time_sec)
        except (TypeError, ValueError):
            time_sec = 0

        def to_float(value):
            try:
                return float(str(value).replace(',', '.'))
            except (TypeError, ValueError):
                return 0.0

        distance_km      = to_float(distance_km)
        huella_distancia = to_float(huella_distancia)
        huella_tiempo    = to_float(huella_tiempo)


        # Item asociado
        item = get_object_or_404(Item, pk=item_id)
        
        cliente = Clientes.objects.get(usuario=request.user)

        # Crear el registro
        registro = Registro.objects.create(
            usuario=cliente,
            item=item,
            time_sec=time_sec,
            dist_km=distance_km,
            huella_dist=huella_distancia,
            huella_time=huella_tiempo,

            timestamp=timezone.now(),
        )

        messages.success(request, "Ecoruta registrada correctamente.")

        # Redirección según el botón
        if action == 'save_add':
            # Volver al mismo formulario para ingresar otra
            return redirect('perfil')   # ajusta al nombre de tu url de creación
        else:
            # Volver al listado de ecorutas
            return redirect('historia_ecorutas')  # ajusta al nombre de tu url de listado

    # GET: mostrar formulario vacío
    items = Item.objects.all()
    return render(request, "ecotracker/perfil.html", {"items": items})


@login_required
def listar_ecoruta(request):
    
    # Usaremos una lista vacía como valor por defecto
    historial_registros = [] 
    
    try:
        # 1. Intentamos obtener el perfil 'Cliente'
        #    Usamos .get() en lugar de get_object_or_404
        cliente = Clientes.objects.get(usuario=request.user)
        
        # 2. Si se encuentra el cliente, filtramos sus registros
        historial_registros = Registro.objects.filter(
            usuario=cliente
        ).order_by('-timestamp')

    except Clientes.DoesNotExist:
        # 3. ¡AQUÍ ESTÁ LA MAGIA!
        #    Si .get() falla porque el Cliente no existe,
        #    atrapamos el error. 'historial_registros'
        #    simplemente se quedará como la lista vacía
        #    que definimos al inicio.
        pass # No hagas nada, la lista ya está vacía.

    # 4. Pasa los registros (vacíos o no) a la plantilla
    context = {
        'registros': historial_registros
    }
    
    # 5. Renderiza la plantilla
    return render(request, 'ecotracker/historia_ecorutas.html', context)