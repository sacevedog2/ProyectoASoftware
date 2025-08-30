from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import AdminCarritoView, CarritoCompraListView, ItemCarritoListView, agregar_al_carrito, quitar_del_carrito, ver_carrito

app_name = "cart"

urlpatterns = [
    # Usuario final: rutas de carrito
    path('carritos/', CarritoCompraListView.as_view(), name='carritocompra_list'),
    path('items/', ItemCarritoListView.as_view(), name='itemcarrito_list'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('ver/', ver_carrito, name='ver_carrito'),
    # Admin: vista protegida solo para staff/admin
    path('admin/carrito/', staff_member_required(AdminCarritoView.as_view()), name='admin_carrito'),
]
