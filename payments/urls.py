from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    AdminPagosView,
    checkout_view,
    procesar_checkout,
    confirmacion_view,
)

app_name = "payments"

urlpatterns = [
    # Flujo de pago para usuarios
    path('checkout/', checkout_view, name='checkout'),
    path('procesar/', procesar_checkout, name='procesar_checkout'),
    path('confirmacion/<int:pago_id>/', confirmacion_view, name='confirmacion'),
    
    # Admin: vista protegida solo para staff/admin
    path('admin/pagos/', staff_member_required(AdminPagosView.as_view()), name='admin_pagos'),
]
