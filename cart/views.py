""""Autor: David Restrepo"""

from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

from catalog.models import Producto
from users.models import Usuario
from .models import CarritoCompra, ItemCarrito


def get_usuario_from_request(request):
    """Helper para obtener el usuario personalizado."""
    return Usuario.objects.filter(correo=request.user.email).first()


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    # Buscar el usuario personalizado
    usuario = get_usuario_from_request(request)
    if not usuario:
        return redirect('home')
    carrito, created = CarritoCompra.objects.get_or_create(usuario=usuario)
    
    # Intentar agregar el producto
    exito = carrito.agregar_producto(producto)
    
    if not exito:
        # Stock insuficiente
        messages.error(request, f'No hay suficiente stock disponible para {producto.nombre}. Stock actual: {producto.stock}')
    else:
        messages.success(request, f'{producto.nombre} agregado al carrito exitosamente')
    
    return redirect('cart:ver_carrito')


@login_required
def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    usuario = get_usuario_from_request(request)
    carrito = CarritoCompra.objects.filter(usuario=usuario).first()
    if carrito:
        carrito.quitar_producto(producto)
    return redirect('cart:ver_carrito')


@login_required
def aumentar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    usuario = get_usuario_from_request(request)
    if not usuario:
        return redirect('home')
    carrito, created = CarritoCompra.objects.get_or_create(usuario=usuario)
    
    # Intentar agregar el producto (aumentar cantidad)
    exito = carrito.agregar_producto(producto)
    
    if not exito:
        # Stock insuficiente
        messages.error(request, f'No hay suficiente stock disponible para {producto.nombre}. Stock actual: {producto.stock}')
    
    return redirect('cart:ver_carrito')


@login_required
def disminuir_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    usuario = get_usuario_from_request(request)
    carrito = CarritoCompra.objects.filter(usuario=usuario).first()
    if carrito:
        # Buscar el item en el carrito
        try:
            item = carrito.items.get(producto=producto)
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
                # Recalcular el total del carrito
                carrito.calcular_total()
            else:
                # Si la cantidad es 1, eliminar el item completamente
                carrito.quitar_producto(producto)
        except ItemCarrito.DoesNotExist:
            pass
    return redirect('cart:ver_carrito')


@login_required
def ver_carrito(request):
    usuario = get_usuario_from_request(request)
    carrito = CarritoCompra.objects.filter(usuario=usuario).first()
    
    items_con_subtotal = []
    if carrito:
        for item in carrito.items.all():
            items_con_subtotal.append({
                'item': item,
                'subtotal': item.cantidad * item.producto.precio
            })
    
    total = carrito.total if carrito else 0
    return render(request, 'cart/ver_carrito.html', {
        'carrito': carrito, 
        'items_con_subtotal': items_con_subtotal, 
        'total': total
    })
