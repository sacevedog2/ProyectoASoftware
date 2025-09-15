""""Autor: David Restrepo"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Pago
from cart.models import CarritoCompra
from orders.models import Pedido, DetallePedido
from users.models import Usuario, Tarjeta


class AdminPagosView(UserPassesTestMixin, ListView):
    """Vista de administración de pagos solo para staff/admin."""
    model = Pago
    template_name = 'payments/admin_pagos.html'
    context_object_name = 'pagos'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return Pago.objects.all().order_by('-fecha_pago')


@login_required
def checkout_view(request):
    """Vista principal de checkout desde el carrito."""
    try:
        # Obtener el usuario personalizado
        usuario = Usuario.objects.filter(correo=request.user.email).first()
        if not usuario:
            messages.error(request, 'Usuario no encontrado')
            return redirect('home')
        
        # Obtener el carrito del usuario
        carrito = CarritoCompra.objects.get(usuario=usuario)
        if not carrito.items.exists():
            messages.error(request, 'Tu carrito está vacío')
            return redirect('cart:ver_carrito')
        
        # Obtener tarjetas del usuario
        tarjetas = Tarjeta.objects.filter(usuario=usuario)
        
        context = {
            'carrito': carrito,
            'items': carrito.items.all(),
            'tarjetas': tarjetas,
            'usuario': usuario,
        }
        
        return render(request, 'payments/checkout.html', context)
        
    except CarritoCompra.DoesNotExist:
        messages.error(request, 'No tienes un carrito activo')
        return redirect('home')


@login_required
def procesar_checkout(request):
    """Procesa el checkout y crea el pedido y pago."""
    if request.method == 'POST':
        try:
            # Obtener el usuario personalizado
            usuario = Usuario.objects.filter(correo=request.user.email).first()
            if not usuario:
                messages.error(request, 'Usuario no encontrado')
                return redirect('home')
            
            # Obtener datos del formulario
            direccion = request.POST.get('direccion')
            nueva_direccion = request.POST.get('nueva_direccion')
            metodo_pago = request.POST.get('metodo_pago')
            tarjeta_id = request.POST.get('tarjeta_id')
            
            # Determinar la dirección a usar
            direccion_final = nueva_direccion if nueva_direccion else direccion
            if not direccion_final:
                messages.error(request, 'Debes proporcionar una dirección de entrega')
                return redirect('payments:checkout')
            
            # Obtener el carrito
            carrito = CarritoCompra.objects.get(usuario=usuario)
            if not carrito.items.exists():
                messages.error(request, 'Tu carrito está vacío')
                return redirect('cart:ver_carrito')
            
            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=usuario,
                estado='pendiente',
                total=carrito.total
            )
            
            # Crear detalles del pedido
            for item in carrito.items.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                    subtotal=item.cantidad * item.producto.precio
                )
            
            # Verificar stock disponible antes de procesar
            stock_insuficiente = []
            for item in carrito.items.all():
                if item.producto.stock < item.cantidad:
                    stock_insuficiente.append(f"{item.producto.nombre} (disponible: {item.producto.stock}, solicitado: {item.cantidad})")
            
            if stock_insuficiente:
                # Si hay stock insuficiente, eliminar el pedido creado y mostrar error
                pedido.delete()
                messages.error(request, f'Stock insuficiente para: {", ".join(stock_insuficiente)}')
                return redirect('payments:checkout')
            
            # Manejar tarjeta si es necesario
            tarjeta_usada = None
            if metodo_pago == 'tarjeta':
                if tarjeta_id:
                    tarjeta_usada = get_object_or_404(Tarjeta, id=tarjeta_id, usuario=usuario)
                else:
                    # Crear nueva tarjeta
                    numero = request.POST.get('numero_tarjeta')
                    tipo = request.POST.get('tipo_tarjeta')
                    fecha_vencimiento = request.POST.get('fecha_vencimiento')
                    
                    if numero and tipo and fecha_vencimiento:
                        tarjeta_usada = Tarjeta.objects.create(
                            usuario=usuario,
                            numero=numero,
                            tipo=tipo,
                            fecha_vencimiento=fecha_vencimiento
                        )
                    else:
                        messages.error(request, 'Datos de tarjeta incompletos')
                        return redirect('payments:checkout')
            
            # Crear el pago
            pago = Pago.objects.create(
                pedido=pedido,
                metodo=metodo_pago,
                monto=carrito.total,
                direccion_entrega=direccion_final,
                tarjeta_usada=tarjeta_usada
            )
            
            # Procesar el pago
            exito = pago.procesar_pago()
            
            if exito:
                # REDUCIR STOCK de los productos comprados
                for item in carrito.items.all():
                    producto = item.producto
                    producto.stock -= item.cantidad
                    producto.save()
                
                # Limpiar el carrito
                carrito.items.all().delete()
                carrito.total = 0
                carrito.save()
                
                # Actualizar estado del pedido
                pedido.estado = 'confirmado'
                pedido.save()
                
                messages.success(request, '¡Pago procesado exitosamente!')
                return redirect('payments:confirmacion', pago_id=pago.id)
            else:
                # Si el pago falla, eliminar el pedido para no afectar el stock
                pedido.delete()
                messages.error(request, 'El pago no pudo ser procesado. Intenta de nuevo.')
                return redirect('payments:checkout')
                
        except CarritoCompra.DoesNotExist:
            messages.error(request, 'No tienes un carrito activo')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error procesando el pago: {str(e)}')
            return redirect('payments:checkout')
    
    return redirect('payments:checkout')


@login_required
def confirmacion_view(request, pago_id):
    """Vista de confirmación del pago."""
    # Obtener el usuario personalizado
    usuario = Usuario.objects.filter(correo=request.user.email).first()
    if not usuario:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    pago = get_object_or_404(
        Pago, 
        id=pago_id, 
        pedido__usuario=usuario
    )
    
    context = {
        'pago': pago,
        'pedido': pago.pedido,
        'items': pago.pedido.detalles.all(),
    }
    
    return render(request, 'payments/confirmacion.html', context)
