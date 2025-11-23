"""
Implementaciones concretas de las interfaces definidas en ``interfaces.py``.

Aquí se ve claramente el principio de Inversión de Dependencias (D de SOLID):
las vistas dependen de estas abstracciones (interfaces) y no directamente
de los modelos o servicios concretos. Si mañana cambiamos la forma de obtener
los productos o las tasas de cambio (por ejemplo, usando otra API), sólo
debemos modificar estas clases y no las vistas.
"""
from catalog.models import Producto
from orders.models import DetallePedido
from catalog.models_historial import HistorialBusqueda

from .interfaces import IProductRepository, ICurrencyService, IRecommendationService
from .currency_service import CurrencyService
from .ranking import productos_mas_vendidos
from .recommendations import productos_recomendados


class DjangoORMProductRepository(IProductRepository):
    """Repositorio de productos basado en el ORM de Django."""

    def get_all_products(self):
        return Producto.objects.all()

    def get_product_by_id(self, product_id):
        try:
            return Producto.objects.get(pk=product_id)
        except Producto.DoesNotExist:
            return None

    def get_top_selling_products(self, top_n: int = 3):
        # Reutilizamos la función existente para mantener una sola fuente de verdad
        return productos_mas_vendidos(top_n=top_n)


class APICurrencyService(ICurrencyService):
    """
    Implementación de ICurrencyService que delega en CurrencyService,
    el cual consume una API externa de tasas de cambio.
    """

    def convert_price(self, price: float, target_currency: str) -> float:
        return CurrencyService.convert_price(price, target_currency)

    def get_supported_currencies(self):
        return CurrencyService.get_supported_currencies()

    def get_exchange_rates(self):
        return CurrencyService.get_exchange_rates()


class RecommendationService(IRecommendationService):
    """
    Implementación de IRecommendationService que utiliza el historial de
    búsqueda y compras del usuario para generar recomendaciones.
    """

    def get_recommendations(self, user, top_n: int = 3):
        # Reutilizamos la lógica existente
        return productos_recomendados(user, top_n=top_n)
