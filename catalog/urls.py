from django.urls import path
from .views import ProductosMasVendidosView, ProductosRecomendadosView, AdminProductosView, ProductoListView, NuevaPublicacionView, ProductoDetailView
from django.contrib.admin.views.decorators import staff_member_required

app_name = "catalog"

urlpatterns = [
    # Usuario final: solo puede ver productos
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('mas-vendidos/', ProductosMasVendidosView.as_view(), name='mas_vendidos'),
    path('recomendados/', ProductosRecomendadosView.as_view(), name='recomendados'),
    # Admin: vista protegida solo para staff/admin
    path('admin/productos/', AdminProductosView.as_view(), name='admin_productos'),
    path('nueva_publicacion/', NuevaPublicacionView.as_view(), name='nueva_publicacion'),
    path('producto/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),
]
