from django.views.generic import FormView
from django.urls import reverse_lazy

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
