from django.contrib import admin
from django.urls import path, include
from .views import HomeView, RecomendacionesView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from catalog.views_currency import CambiarMonedaView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Para cambio de idioma
    path('cambiar-moneda/', CambiarMonedaView.as_view(), name='cambiar_moneda'),  # Cambio de moneda sin prefijo de idioma
    path('api/', include('catalog.api_urls')),  # API REST de productos (sin prefijo de idioma)
]

# URLs con soporte de idioma
urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home'),
    path('recomendaciones/', RecomendacionesView.as_view(), name='recomendaciones'),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("users/", include("users.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
    prefix_default_language=True,  # Agregar prefijo de idioma en las URLs
)

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
