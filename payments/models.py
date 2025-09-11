from django.db import models

class Pago(models.Model):
	"""
	Modelo para los pagos realizados por los usuarios.
	"""
	pedido = models.ForeignKey('orders.Pedido', on_delete=models.CASCADE, related_name='pagos')
	fecha_pago = models.DateTimeField(auto_now_add=True)
	metodo = models.CharField(max_length=30)
	monto = models.FloatField(default=0.0)
	estado = models.CharField(max_length=30)

	class Meta:
		verbose_name = 'Pago'
		verbose_name_plural = 'Pagos'

	def __str__(self):
		return f"Pago({self.pk}, Pedido: {self.pedido_id}, Monto: {self.monto})"

	def procesar_pago(self):
		# Implementar lógica para procesar el pago
		pass
