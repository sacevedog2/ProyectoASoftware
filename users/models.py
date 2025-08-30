
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

	def clean(self):
		# Validaciones complejas aquí
		pass

	def registrarse(self):
		"""Registra un nuevo usuario en el sistema."""
		# Implementar lógica de registro
		pass

	def iniciar_sesion(self, contrasena):
		# Implementar lógica de inicio de sesión
		pass

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

	def ultimos_4(self):
		return self.numero[-4:]

	def __str__(self):
		return f"{self.get_tipo_display()} ****{self.ultimos_4()}"

	class Meta:
		verbose_name = _('Tarjeta')
		verbose_name_plural = _('Tarjetas')

	def __str__(self):
		return f"{self.nombre} ({self.correo})"

	def clean(self):
		# Validaciones complejas aquí
		pass

	def registrarse(self):
		"""Registra un nuevo usuario en el sistema."""
		# Implementar lógica de registro
		pass

	def iniciar_sesion(self, contrasena):
		"""Inicia sesión si la contraseña es correcta."""
		return self.contrasena == contrasena

	def actualizar_perfil(self, **kwargs):
		"""Actualiza los datos del perfil del usuario."""
		for key, value in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, value)
		self.save()
