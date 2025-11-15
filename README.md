# 🌱 EcoTracker

Un proyecto Django para el seguimiento y registro de actividades ecológicas y consumo de recursos.

## 📋 Descripción

EcoTracker es una aplicación web que permite a los usuarios:
- Registrarse y crear perfiles personalizados
- Registrar el uso de vehículos y actividades
- Calcular la huella de carbono basada en el consumo de recursos
- Visualizar estadísticas y datos de sostenibilidad

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- pip o pipenv
- Django 3.2+

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Los-5-Fantasticos/EcoTracker.git
   cd EcoTracker
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En macOS/Linux
   # o
   .venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Crear superuser (administrador):**
   ```bash
   python manage.py createsuperuser
   # O ejecutar el script:
   python scripts/create_superuser.py
   ```

6. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación:**
   - Sitio: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 📁 Estructura del Proyecto

```
EcoTracker/
├── Eco_Tracker/           # App principal de Django
│   ├── migrations/        # Migraciones de base de datos
│   ├── templates/         # Templates HTML
│   ├── models.py          # Modelos de datos (Item, Clientes, Registro)
│   ├── views.py           # Vistas y lógica de negocio
│   ├── urls.py            # Rutas de la app
│   └── admin.py           # Configuración del admin de Django
├── EcoTracker/            # Configuración del proyecto Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py            # Rutas principales
│   ├── wsgi.py            # WSGI para producción
│   └── asgi.py            # ASGI para producción
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── scripts/               # Scripts útiles
├── manage.py              # Utilidad de administración de Django
├── db.sqlite3             # Base de datos (desarrollo)
└── .gitignore             # Archivos a ignorar en Git
```

## 📊 Modelos de Datos

### Item
- Código de item
- Nombre
- Descripción
- Factor de emisión (para cálculo de huella de carbono)

### Clientes
- Código del cliente
- Usuario (FK a auth.User)
- Nombre y apellido
- Dirección
- RUT
- Teléfono
- Email de contacto

### Registro
- Código del registro
- Item (FK)
- Tiempo en segundos
- Huella de carbono por tiempo
- Distancia en km
- Huella de carbono por distancia
- Usuario/Cliente (FK)
- Timestamp

## 🔐 Autenticación

- Registro de nuevos usuarios
- Login/Logout con sesiones Django
- Decoradores `@login_required` para rutas protegidas
- Validación de email y username únicos

## 🛠 Tecnologías

- **Backend**: Django 3.2+
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (recomendado para producción)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Autenticación**: Django auth

## 📝 TODO

Ver `TODO.md` para una lista de tareas pendientes del proyecto.

## 👥 Equipo

**Los 5 Fantásticos**

## 📄 Licencia

Proyecto educativo. Todos los derechos reservados.

---

**Última actualización**: 15 de noviembre de 2025
