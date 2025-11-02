from django.db import models
from django.conf import settings  # 1. Importa la configuración de Django

# Create your models here.
class Item(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    factor = models.FloatField()

    def __str__(self):
        return self.name
    
class Clientes(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    # --- ESTA ES LA LÍNEA CORREGIDA ---
    # Usamos settings.AUTH_USER_MODEL para referirnos al modelo de usuario
    # que esté activo en el proyecto (por defecto, 'auth.User').
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # ¿Qué hacer si se borra el usuario? CASCADE = Borrar también este cliente
        related_name='cliente'    # Opcional: permite acceder desde user.cliente
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    rut = models.CharField(max_length=12, unique=True)
    telephone = models.CharField(max_length=15)
    email_contacto = models.EmailField(unique=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Registro(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    time_sec = models.IntegerField()
    huella = models.FloatField()
    usuario = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro {self.codigo} for Item {self.item.name}"
    
    