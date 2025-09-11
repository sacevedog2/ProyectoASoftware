from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Inventario

# Vista de administración de inventario (solo staff/admin)
class AdminInventarioView(UserPassesTestMixin, ListView):
	"""Vista de administración de inventario solo para staff/admin."""
	model = Inventario
	template_name = 'inventory/admin_inventario.html'
	context_object_name = 'inventarios'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Inventario.objects.all()
