
"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Vistas para historial y PDF de facturas.
"""
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Pedido
from .services.pdf_utils import generar_factura_pdf

class HistorialPedidosView(LoginRequiredMixin, ListView):
	"""Muestra el historial de compras del usuario."""
	model = Pedido
	template_name = 'orders/historial.html'
	context_object_name = 'pedidos'

	def get_queryset(self):
		from users.models import Usuario
		try:
			usuario_custom = Usuario.objects.get(correo=self.request.user.email)
			return Pedido.objects.filter(usuario=usuario_custom)
		except Usuario.DoesNotExist:
			return Pedido.objects.none()

class FacturaPDFView(LoginRequiredMixin, View):
	"""Genera y retorna el PDF de la factura de un pedido."""
	def get(self, request, pedido_id):
		pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
		return generar_factura_pdf(pedido)

# Vista de administración de pedidos (solo staff/admin)
class AdminPedidosView(UserPassesTestMixin, ListView):
	"""Vista de administración de pedidos solo para staff/admin."""
	model = Pedido
	template_name = 'orders/admin_pedidos.html'
	context_object_name = 'pedidos'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Pedido.objects.all()
