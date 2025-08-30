from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import AdminPagosView

app_name = "payments"

urlpatterns = [
    # Usuario final: rutas de pagos
    # path('pagar/', login_required(PagoView.as_view()), name='pagar'),
    # Admin: vista protegida solo para staff/admin
    path('admin/pagos/', staff_member_required(AdminPagosView.as_view()), name='admin_pagos'),
]
