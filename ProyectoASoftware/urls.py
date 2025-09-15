from django.contrib import admin
from django.urls import path, include
from .views import HomeView, RecomendacionesView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recomendaciones/', RecomendacionesView.as_view(), name='recomendaciones'),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("users/", include("users.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
