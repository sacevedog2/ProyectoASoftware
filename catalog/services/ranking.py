"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Servicio para obtener productos más vendidos.
"""
from catalog.models import Producto
from orders.models import DetallePedido
from django.db.models import Sum

def productos_mas_vendidos(top_n=3):
    """Retorna los productos más vendidos."""
    productos = Producto.objects.annotate(
        total_vendidos=Sum('detalles_pedido__cantidad')
    ).filter(total_vendidos__gte=2).order_by('-total_vendidos')[:top_n]
    return productos
