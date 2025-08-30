from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from catalog.models import Producto
from users.models import Usuario

@login_required
def agregar_al_carrito(request, producto_id):
	producto = get_object_or_404(Producto, pk=producto_id)
	# Buscar el usuario personalizado
	usuario = Usuario.objects.filter(correo=request.user.email).first()
	if not usuario:
		return redirect('home')
	carrito, _ = CarritoCompra.objects.get_or_create(usuario=usuario)
	carrito.agregar_producto(producto)
	return redirect('cart:ver_carrito')

@login_required
def quitar_del_carrito(request, producto_id):
	producto = get_object_or_404(Producto, pk=producto_id)
	usuario = Usuario.objects.filter(correo=request.user.email).first()
	carrito = CarritoCompra.objects.filter(usuario=usuario).first()
	if carrito:
		carrito.quitar_producto(producto)
	return redirect('cart:ver_carrito')

@login_required
def ver_carrito(request):
	usuario = Usuario.objects.filter(correo=request.user.email).first()
	carrito = CarritoCompra.objects.filter(usuario=usuario).first()
	items = carrito.items.all() if carrito else []
	total = carrito.total if carrito else 0
	return render(request, 'cart/ver_carrito.html', {'carrito': carrito, 'items': items, 'total': total})
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import CarritoCompra, ItemCarrito

# Vista de administración de carrito (solo staff/admin)
class AdminCarritoView(UserPassesTestMixin, ListView):
	"""Vista de administración de carritos solo para staff/admin."""
	model = CarritoCompra
	template_name = 'cart/admin_carrito.html'
	context_object_name = 'carritos'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return CarritoCompra.objects.all()

# Vista para listar carritos
class CarritoCompraListView(ListView):
	model = CarritoCompra
	template_name = 'cart/carritocompra_list.html'
	context_object_name = 'carritos'

# Vista para listar items del carrito
class ItemCarritoListView(ListView):
	model = ItemCarrito
	template_name = 'cart/itemcarrito_list.html'
	context_object_name = 'items'
