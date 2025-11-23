"""
Vistas API de solo lectura para el catálogo de productos en formato JSON
"""

from django.http import JsonResponse
from django.views import View
from .models import Producto


class ProductoListAPIView(View):
    """
    API endpoint que devuelve la lista de todos los productos en formato JSON.
    GET /api/productos/ - Lista todos los productos
    """
    
    def get(self, request):
        """Devuelve todos los productos en formato JSON."""
        productos = Producto.objects.all()
        
        # Serializar productos a diccionarios
        productos_data = []
        for producto in productos:
            productos_data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'stock': producto.stock,
                'talla': producto.talla,
                'tallas_disponibles': producto.tallas_list,
                'color': producto.color,
                'tipo': producto.tipo,
                'genero': producto.genero,
                'imagen': producto.imagen.url if producto.imagen else None,
            })
        
        return JsonResponse({
            'success': True,
            'count': len(productos_data),
            'productos': productos_data
        }, safe=False)


class ProductoDetailAPIView(View):
    """
    API endpoint que devuelve los detalles de un producto específico.
    GET /api/productos/<id>/ - Obtiene detalles de un producto
    """
    
    def get(self, request, pk):
        """Devuelve los detalles de un producto en formato JSON."""
        try:
            producto = Producto.objects.get(pk=pk)
            
            producto_data = {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'stock': producto.stock,
                'talla': producto.talla,
                'tallas_disponibles': producto.tallas_list,
                'color': producto.color,
                'tipo': producto.tipo,
                'tipo_display': producto.get_tipo_display(),
                'genero': producto.genero,
                'genero_display': producto.get_genero_display(),
                'imagen': producto.imagen.url if producto.imagen else None,
            }
            
            return JsonResponse({
                'success': True,
                'producto': producto_data
            })
            
        except Producto.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Producto no encontrado'
            }, status=404)


class ProductoSearchAPIView(View):
    """
    API endpoint para buscar productos por criterios.
    GET /api/productos/buscar/?q=texto&tipo=camiseta&genero=hombre
    """
    
    def get(self, request):
        """Busca productos según parámetros de consulta."""
        productos = Producto.objects.all()
        
        # Filtrar por búsqueda de texto
        query = request.GET.get('q', '')
        if query:
            productos = productos.filter(nombre__icontains=query)
        
        # Filtrar por tipo
        tipo = request.GET.get('tipo', '')
        if tipo:
            productos = productos.filter(tipo=tipo)
        
        # Filtrar por género
        genero = request.GET.get('genero', '')
        if genero:
            productos = productos.filter(genero=genero)
        
        # Filtrar por rango de precio
        precio_min = request.GET.get('precio_min', '')
        if precio_min:
            productos = productos.filter(precio__gte=float(precio_min))
        
        precio_max = request.GET.get('precio_max', '')
        if precio_max:
            productos = productos.filter(precio__lte=float(precio_max))
        
        # Serializar resultados
        productos_data = []
        for producto in productos:
            productos_data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'stock': producto.stock,
                'talla': producto.talla,
                'color': producto.color,
                'tipo': producto.tipo,
                'genero': producto.genero,
                'imagen': producto.imagen.url if producto.imagen else None,
            })
        
        return JsonResponse({
            'success': True,
            'count': len(productos_data),
            'filtros': {
                'q': query,
                'tipo': tipo,
                'genero': genero,
                'precio_min': precio_min,
                'precio_max': precio_max,
            },
            'productos': productos_data
        })
