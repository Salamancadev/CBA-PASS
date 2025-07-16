from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('administrativo', 'Administrativo'),
        ('visitante', 'Visitante'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', null=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class QR(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='qr')
    codigo = models.CharField(max_length=255, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR de {self.usuario}"

class HistorialAcceso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo_evento = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])

    def __str__(self):
        return f"{self.usuario} - {self.tipo_evento} - {self.fecha_hora}"