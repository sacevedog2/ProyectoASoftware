from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import AdminInventarioView

app_name = "inventory"

urlpatterns = [
    # Usuario final: rutas de inventario (si aplica)
    # Admin: ejemplo de vista protegida (se implementará en views.py)
    # Admin: vista protegida solo para staff/admin
    path('admin/inventario/', staff_member_required(AdminInventarioView.as_view()), name='admin_inventario'),
]
