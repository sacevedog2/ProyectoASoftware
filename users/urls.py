from django.urls import path
from django.contrib.auth import views as auth_views
from .email_auth_form import EmailAuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from .views import AdminUsuariosView, EditarPerfilView, EliminarCuentaView, VerPerfilView, TarjetasView, VincularTarjetaView
from .auth_views import RegistroView

app_name = "users"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegistroView.as_view(), name='register'),
    # Admin: vista protegida solo para staff/admin
    path('admin/usuarios/', staff_member_required(AdminUsuariosView.as_view()), name='admin_usuarios'),
    path('editar/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('perfil/', VerPerfilView.as_view(), name='ver_perfil'),
    path('eliminar/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
    path('tarjetas/', TarjetasView.as_view(), name='tarjetas'),
    path('tarjetas/vincular/', VincularTarjetaView.as_view(), name='vincular_tarjeta'),
]
