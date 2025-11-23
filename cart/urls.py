from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import agregar_al_carrito, quitar_del_carrito, ver_carrito, aumentar_cantidad, disminuir_cantidad

app_name = "cart"

urlpatterns = [
    # Usuario final: rutas de carrito
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('aumentar/<int:producto_id>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir/<int:producto_id>/', disminuir_cantidad, name='disminuir_cantidad'),
    path('ver/', ver_carrito, name='ver_carrito'),
]
