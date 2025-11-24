"""API mínima: retorna lista plana con campos aliados."""

from django.http import JsonResponse
from django.views import View
from .models import Producto


class ProductoListadoPlanoAPIView(View):
    """GET /api/productos/ -> lista plana de productos con campos estilo aliado."""

    def get(self, request):
        productos = Producto.objects.all()
        resultado = []
        for p in productos:
            resultado.append({
                'idProducto': p.id,
                'nombreProducto': p.nombre,
                'tipoProducto': p.tipo,
                'marcaProducto': p.color,  # reutilizamos color como marca si no existe marca
                'cantidadDeProducto': p.stock,
                'fechaVencimientoProducto': None,  # no disponible en modelo
                'precioDeProducto': p.precio,
                'imagenProducto': p.imagen.url if p.imagen else None,
            })
        return JsonResponse(resultado, safe=False)


