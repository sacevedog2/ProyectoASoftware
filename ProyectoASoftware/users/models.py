
"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Modelo Usuario para ProyectoASoftware
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Usuario(models.Model):
	"""
	Modelo de usuario para el sistema.
	Representa los datos y operaciones de un usuario.
	"""
	nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
	correo = models.EmailField(unique=True, verbose_name=_('Correo electrónico'))
	contrasena = models.CharField(max_length=128, verbose_name=_('Contraseña'))
	direccion = models.CharField(max_length=255, verbose_name=_('Dirección'))
	telefono = models.CharField(max_length=20, verbose_name=_('Teléfono'))
	rol = models.BooleanField(default=False, verbose_name=_('Rol administrador'))

	class Meta:
		ordering = ['nombre']
		verbose_name = _('Usuario')
		verbose_name_plural = _('Usuarios')

	def __str__(self):
		return f"{self.nombre} ({self.correo})"

class Tarjeta(models.Model):
    TIPO_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express'),
        ('otro', 'Otro'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tarjetas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=16)
    fecha_vencimiento = models.CharField(max_length=5)  # MM/YY

    class Meta:
        verbose_name = _('Tarjeta')
        verbose_name_plural = _('Tarjetas')

    def ultimos_4(self):
        return self.numero[-4:]

    def __str__(self):
        return f"{self.get_tipo_display()} ****{self.ultimos_4()}"
