
from django.db import models

class Pedido(models.Model):
	"""
	Modelo para los pedidos realizados por los usuarios.
	"""
	usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='pedidos')
	fecha_pedido = models.DateTimeField(auto_now_add=True)
	estado = models.CharField(max_length=30)
	total = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'

	def __str__(self):
		return f"Pedido({self.pk}, Usuario: {self.usuario_id}, Total: {self.total})"

	def generar_factura(self):
		# Implementar lógica para generar factura
		pass

	def actualizar_estado(self, nuevo_estado):
		self.estado = nuevo_estado
		self.save()

class DetallePedido(models.Model):
	"""
	Modelo para el detalle de cada pedido.
	"""
	pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='detalles')
	producto = models.ForeignKey('catalog.Producto', on_delete=models.CASCADE, related_name='detalles_pedido')
	cantidad = models.PositiveIntegerField(default=1)
	precio_unitario = models.FloatField()
	subtotal = models.FloatField()

	class Meta:
		verbose_name = 'Detalle de pedido'
		verbose_name_plural = 'Detalles de pedido'

	def __str__(self):
		return f"DetallePedido({self.pk}, Pedido: {self.pedido_id}, Producto: {self.producto_id})"

	def calcular_subtotal(self):
		self.subtotal = self.cantidad * self.precio_unitario
		return self.subtotal
