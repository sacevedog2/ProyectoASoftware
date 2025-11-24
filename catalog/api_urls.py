"""URLs para la API mínima de productos (lista plana)."""
from django.urls import path
from .api_views import ProductoListadoPlanoAPIView

app_name = "api"

urlpatterns = [
    path('productos/', ProductoListadoPlanoAPIView.as_view(), name='producto_listado_plano'),
]
