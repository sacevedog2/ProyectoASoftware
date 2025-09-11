from django.db import models

class Inventario(models.Model):
	producto = models.ForeignKey('catalog.Producto', on_delete=models.CASCADE, related_name='inventarios')
	cantidad = models.PositiveIntegerField(default=0)
	ubicacion = models.CharField(max_length=100)

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventarios'

	def __str__(self):
		return f"Inventario({self.pk}, Producto: {self.producto.nombre}, Cantidad: {self.cantidad})"
