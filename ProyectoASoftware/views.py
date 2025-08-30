from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from catalog.models import Producto

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        from catalog.services.ranking import productos_mas_vendidos
        from catalog.models_historial import HistorialBusqueda
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        tipo = self.request.GET.get('tipo', '')
        genero = self.request.GET.get('genero', '')
        productos = Producto.objects.all()
        if q:
            productos = productos.filter(nombre__icontains=q)
        if tipo:
            productos = productos.filter(tipo=tipo)
        if genero:
            productos = productos.filter(genero=genero)
        # Registrar búsqueda si el usuario está autenticado y hay algún filtro
        if self.request.user.is_authenticated and (q or tipo or genero):
            from users.models import Usuario
            try:
                usuario_custom = Usuario.objects.get(correo=self.request.user.email)
                HistorialBusqueda.objects.create(
                    usuario=usuario_custom,
                    termino=q,
                    tipo=tipo,
                    genero=genero
                )
            except Usuario.DoesNotExist:
                pass
        context["productos"] = productos
        context["user"] = self.request.user
        context["q"] = q
        context["tipo"] = tipo
        context["genero"] = genero
        # Ranking de productos más vendidos
        context["ranking"] = productos_mas_vendidos(top_n=3)
        return context

# Vista de recomendaciones aparte
class RecomendacionesView(LoginRequiredMixin, TemplateView):
    template_name = "recomendaciones.html"

    def get_context_data(self, **kwargs):
        from catalog.services.recommendations import productos_recomendados
        context = super().get_context_data(**kwargs)
        from users.models import Usuario
        try:
            usuario_custom = Usuario.objects.get(correo=self.request.user.email)
            context["recomendados"] = productos_recomendados(usuario_custom, top_n=3)
        except Usuario.DoesNotExist:
            context["recomendados"] = []
        return context
