from django.urls import path
from .views import AdminProductosView, NuevaPublicacionView, ProductoDetailView, ProductoEditView
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import RedirectView

app_name = "catalog"

urlpatterns = [
    path('productos/', RedirectView.as_view(url='/', permanent=True), name='producto_list_redirect'),
    # Admin: vista protegida solo para staff/admin
    path('admin/productos/', AdminProductosView.as_view(), name='admin_productos'),
    path('nueva_publicacion/', NuevaPublicacionView.as_view(), name='nueva_publicacion'),
    path('producto/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),
    path('producto/<int:pk>/editar/', staff_member_required(ProductoEditView.as_view()), name='editar_producto'),
]
