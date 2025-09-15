"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Vistas para productos más vendidos y recomendaciones.
"""
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Producto
from .services.ranking import productos_mas_vendidos
from .services.recommendations import productos_recomendados

# Vista de detalle de producto
class ProductoDetailView(DetailView):
	model = Producto
	template_name = 'catalog/detalle_producto.html'
	context_object_name = 'producto'

# Vista de edición de producto para administradores
class ProductoEditView(UserPassesTestMixin, UpdateView):
	"""Vista de edición de producto solo para staff/admin."""
	model = Producto
	template_name = 'catalog/editar_producto.html'
	fields = ['nombre', 'descripcion', 'precio', 'stock', 'talla', 'color', 'tipo', 'genero', 'imagen']
	context_object_name = 'producto'
	success_url = reverse_lazy('home')

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def form_valid(self, form):
		response = super().form_valid(form)
		from django.contrib import messages
		messages.success(self.request, f'Producto "{form.instance.nombre}" actualizado exitosamente!')
		return response
	
# Vista para crear nueva publicación
class NuevaPublicacionView(CreateView):
	model = Producto
	template_name = 'catalog/nueva_publicacion.html'
	fields = ['nombre', 'descripcion', 'precio', 'stock', 'talla', 'color', 'tipo', 'genero', 'imagen']
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		# Guardar varias tallas seleccionadas como texto separado por comas
		tallas = self.request.POST.getlist('talla')
		form.instance.talla = ','.join(tallas)
		response = super().form_valid(form)
		from django.contrib import messages
		messages.success(self.request, '¡Publicación creada exitosamente!')
		return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

# Vista de administración de productos (solo staff/admin)
class AdminProductosView(UserPassesTestMixin, ListView):
	"""Vista de administración de productos solo para staff/admin."""
	model = Producto
	template_name = 'catalog/admin_productos.html'
	context_object_name = 'productos'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Producto.objects.all()
