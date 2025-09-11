from django.views.generic import DetailView
from .models import Producto
# Vista de detalle de producto
class ProductoDetailView(DetailView):
	model = Producto
	template_name = 'catalog/detalle_producto.html'
	context_object_name = 'producto'

"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Vistas para productos más vendidos y recomendaciones.
"""
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Producto
from django.urls import reverse_lazy
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
from .services.ranking import productos_mas_vendidos
from .services.recommendations import productos_recomendados

class ProductosMasVendidosView(ListView):
	"""Muestra los productos más vendidos."""
	model = Producto
	template_name = 'catalog/mas_vendidos.html'
	context_object_name = 'productos'

	def get_queryset(self):
		return productos_mas_vendidos()

# Vista para listar productos
class ProductoListView(ListView):
	model = Producto
	template_name = 'catalog/producto_list.html'
	context_object_name = 'productos'

class ProductosRecomendadosView(LoginRequiredMixin, ListView):
	"""Muestra productos recomendados para el usuario."""
	model = Producto
	template_name = 'catalog/recomendados.html'
	context_object_name = 'productos'

	def get_queryset(self):
		return productos_recomendados(self.request.user)

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
