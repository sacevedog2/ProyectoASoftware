from django.db import models
from users.models import Usuario

class HistorialBusqueda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='busquedas')
    termino = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, blank=True, null=True)
    genero = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} buscó '{self.termino}' ({self.tipo}, {self.genero})"
