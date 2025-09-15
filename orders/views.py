
"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Vistas para historial y PDF de facturas.
"""
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
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
		from users.models import Usuario
		try:
			usuario_custom = Usuario.objects.get(correo=request.user.email)
			pedido = get_object_or_404(Pedido, id=pedido_id, usuario=usuario_custom)
			return generar_factura_pdf(pedido)
		except Usuario.DoesNotExist:
			return HttpResponse("Usuario no encontrado", status=404)

# Vista de administración de pedidos (solo staff/admin)
class AdminPedidosView(UserPassesTestMixin, ListView):
	"""Vista de administración de pedidos solo para staff/admin."""
	model = Pedido
	template_name = 'orders/admin_pedidos.html'
	context_object_name = 'pedidos'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Pedido.objects.all().order_by('-fecha_pedido')

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def actualizar_estado_pedido(request, pedido_id):
	"""Vista para actualizar el estado de un pedido (solo admin)."""
	if request.method == 'POST':
		pedido = get_object_or_404(Pedido, id=pedido_id)
		nuevo_estado = request.POST.get('estado')
		
		if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
			pedido.actualizar_estado(nuevo_estado)
			messages.success(request, f'Estado del pedido #{pedido.pk} actualizado a "{pedido.get_estado_display()}"')
		else:
			messages.error(request, 'Estado inválido')
	
	return redirect('orders:admin_pedidos')
