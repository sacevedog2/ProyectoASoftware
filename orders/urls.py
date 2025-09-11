from django.urls import path
from .views import HistorialPedidosView, FacturaPDFView, AdminPedidosView
from django.contrib.admin.views.decorators import staff_member_required

app_name = "orders"

urlpatterns = [
    # Usuario final: historial y facturas
    path('historial/', HistorialPedidosView.as_view(), name='historial'),
    path('factura/<int:pedido_id>/', FacturaPDFView.as_view(), name='factura_pdf'),
    # Admin: vista protegida solo para staff/admin
    path('admin/pedidos/', AdminPedidosView.as_view(), name='admin_pedidos'),
]
