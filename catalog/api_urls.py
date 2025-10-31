"""
URLs para la API REST de productos (solo lectura)
"""
from django.urls import path
from .api_views import (
    ProductoListAPIView,
    ProductoDetailAPIView,
    ProductoSearchAPIView,
)

app_name = "api"

urlpatterns = [
    # Listar todos los productos
    path('productos/', ProductoListAPIView.as_view(), name='producto_list'),
    
    # Buscar productos
    path('productos/buscar/', ProductoSearchAPIView.as_view(), name='producto_search'),
    
    # Detalle de un producto específico
    path('productos/<int:pk>/', ProductoDetailAPIView.as_view(), name='producto_detail'),
]
