from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Pago

# Vista de administración de pagos (solo staff/admin)
class AdminPagosView(UserPassesTestMixin, ListView):
	"""Vista de administración de pagos solo para staff/admin."""
	model = Pago
	template_name = 'payments/admin_pagos.html'
	context_object_name = 'pagos'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Pago.objects.all()
