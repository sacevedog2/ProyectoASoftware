
"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Modelo Producto para ProyectoASoftware
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class Producto(models.Model):
	@property
	def tallas_list(self):
		return self.talla.split(',') if self.talla else []
	"""
	Modelo de producto para el catálogo.
	Representa los datos y operaciones de un producto.
	"""
	nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
	descripcion = models.TextField(verbose_name=_('Descripción'))
	precio = models.FloatField(verbose_name=_('Precio'))
	stock = models.PositiveIntegerField(verbose_name=_('Stock'))
	talla = models.CharField(max_length=20, verbose_name=_('Talla'))
	color = models.CharField(max_length=30, verbose_name=_('Color'))
	tipo = models.CharField(max_length=30, choices=[('camiseta','Camiseta'),('buzo','Buzo'),('pantalon','Pantalón')], default='camiseta', verbose_name=_('Tipo de prenda'))
	genero = models.CharField(max_length=10, choices=[('hombre','Hombre'),('mujer','Mujer')], default='hombre', verbose_name=_('Género'))
	imagen = models.ImageField(upload_to='productos/', verbose_name=_('Imagen del producto'), null=True, blank=True)

	class Meta:
		ordering = ['nombre']
		verbose_name = _('Producto')
		verbose_name_plural = _('Productos')

	def __str__(self):
		return f"{self.nombre}"

	def clean(self):
		# Validaciones complejas aquí
		pass

	def actualizar_stock(self, cantidad):
		"""Actualiza el stock del producto."""
		self.stock = cantidad
		self.save()

	def actualizar_precio(self, nuevo_precio):
		"""Actualiza el precio del producto."""
		self.precio = nuevo_precio
		self.save()
