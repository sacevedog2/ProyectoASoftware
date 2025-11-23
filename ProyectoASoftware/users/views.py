from django.shortcuts import redirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View

from .models import Tarjeta, Usuario


class VincularTarjetaView(LoginRequiredMixin, CreateView):
    model = Tarjeta
    template_name = 'users/vincular_tarjeta.html'
    fields = ['tipo', 'numero', 'fecha_vencimiento']
    success_url = '/users/tarjetas/'

    def form_valid(self, form):
        # Obtener el usuario personalizado
        usuario = Usuario.objects.filter(correo=self.request.user.email).first()
        if usuario:
            form.instance.usuario = usuario
        return super().form_valid(form)
    
# Vista para mostrar tarjetas vinculadas
class TarjetasView(LoginRequiredMixin, ListView):
    model = Tarjeta
    template_name = 'users/tarjetas.html'
    context_object_name = 'tarjetas'

    def get_queryset(self):
        return Tarjeta.objects.filter(usuario__correo=self.request.user.email)

# Vista para ver perfil de usuario
class VerPerfilView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'users/ver_perfil.html'
    context_object_name = 'usuario'

    def get_object(self, queryset=None):
        usuario = Usuario.objects.filter(correo=self.request.user.email).first()
        if not usuario:
            return redirect('home')
        return usuario

# Vista para eliminar cuenta
class EliminarCuentaView(LoginRequiredMixin, View):
    def post(self, request):
        # Eliminar usuario estándar y personalizado
        user = request.user
        try:
            usuario_custom = Usuario.objects.filter(correo=user.email).first()
            if usuario_custom:
                usuario_custom.delete()
        except Usuario.DoesNotExist:
            pass
        user.delete()
        logout(request)
        return redirect('/users/register/')

# Vista de administración de usuarios (solo staff/admin)
class AdminUsuariosView(UserPassesTestMixin, ListView):
    """Vista de administración de usuarios solo para staff/admin."""
    model = get_user_model()
    template_name = 'users/admin_usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return self.model.objects.all()


# Vista para editar perfil de usuario
class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'users/editar_perfil.html'
    fields = ['nombre', 'direccion', 'telefono']
    
    def get_object(self, queryset=None):
        return Usuario.objects.filter(correo=self.request.user.email).first()
    
    def get_success_url(self):
        return '/users/perfil/'
