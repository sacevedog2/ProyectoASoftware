
from django.db import models

class Pedido(models.Model):
	"""
	Modelo para los pedidos realizados por los usuarios.
	"""
	
	ESTADO_CHOICES = [
		('pendiente', 'Pendiente'),
		('confirmado', 'Confirmado'),
		('en_proceso', 'En proceso de preparación'),
		('en_camino', 'En camino'),
		('entregado', 'Entregado'),
		('cancelado', 'Cancelado'),
	]
	
	usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='pedidos')
	fecha_pedido = models.DateTimeField(auto_now_add=True)
	estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
	total = models.FloatField(default=0.0)

	class Meta:
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'
		ordering = ['-fecha_pedido']

	def __str__(self):
		return f"Pedido #{self.pk} - {self.usuario.nombre} - {self.get_estado_display()}"

	def actualizar_estado(self, nuevo_estado):
		self.estado = nuevo_estado
		self.save()
	
	def get_estado_color(self):
		"""Retorna un color para el estado del pedido"""
		colores = {
			'pendiente': 'warning',
			'confirmado': 'info',
			'en_proceso': 'primary',
			'en_camino': 'secondary',
			'entregado': 'success',
			'cancelado': 'danger',
		}
		return colores.get(self.estado, 'secondary')
	
	def get_estado_icon(self):
		"""Retorna un icono para el estado del pedido"""
		iconos = {
			'pendiente': 'fas fa-clock',
			'confirmado': 'fas fa-check-circle',
			'en_proceso': 'fas fa-cog fa-spin',
			'en_camino': 'fas fa-truck',
			'entregado': 'fas fa-check-double',
			'cancelado': 'fas fa-times-circle',
		}
		return iconos.get(self.estado, 'fas fa-question-circle')

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
