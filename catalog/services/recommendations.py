"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Servicio para recomendaciones personalizadas de productos.
"""
from catalog.models import Producto
from orders.models import Pedido, DetallePedido
from catalog.models_historial import HistorialBusqueda

def productos_recomendados(usuario, top_n=3):
    """Sugiere productos según el historial de búsqueda del usuario."""
    # Buscar los términos y filtros más recientes del usuario
    busquedas = HistorialBusqueda.objects.filter(usuario=usuario).order_by('-fecha')[:5]
    productos = Producto.objects.all()
    filtros = {}
    for b in busquedas:
        if b.termino:
            productos = productos.filter(nombre__icontains=b.termino)
        if b.tipo:
            productos = productos.filter(tipo=b.tipo)
        if b.genero:
            productos = productos.filter(genero=b.genero)
    # Excluir productos ya comprados
    productos_comprados = DetallePedido.objects.filter(pedido__usuario=usuario).values_list('producto', flat=True)
    recomendados = productos.exclude(id__in=productos_comprados).distinct()[:top_n]
    return recomendados
