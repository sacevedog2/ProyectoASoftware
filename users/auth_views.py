from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

class RegistroView(FormView):
    template_name = "users/registro.html"
    from .forms import CustomUserCreationForm
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        # Crear instancia de Usuario personalizada
        from .models import Usuario
        Usuario.objects.create(
            nombre=user.username,
            correo=user.email,
            contrasena=user.password,
            direccion="",
            telefono="",
            rol=False
        )
        return super().form_valid(form)

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())
