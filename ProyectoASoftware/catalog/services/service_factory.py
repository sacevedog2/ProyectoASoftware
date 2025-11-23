"""
Factory para crear instancias de servicios (patrón Factory) junto con
el uso de interfaces para demostrar Inversión de Dependencias.
"""
from .implementations import (
    DjangoORMProductRepository,
    APICurrencyService,
    RecommendationService,
)
from .interfaces import IProductRepository, ICurrencyService, IRecommendationService


class ServiceFactory:
    """
    Factory para crear instancias de servicios.

    Las vistas pueden solicitar los servicios a esta clase sin conocer
    la implementación concreta. Si mañana cambiamos de ORM o de API de monedas,
    sólo modificamos esta factory y/o las implementaciones, manteniendo
    el resto del código intacto.
    """

    @staticmethod
    def get_product_repository() -> IProductRepository:
        """Retorna un repositorio de productos."""
        return DjangoORMProductRepository()

    @staticmethod
    def get_currency_service() -> ICurrencyService:
        """Retorna el servicio de monedas."""
        return APICurrencyService()

    @staticmethod
    def get_recommendation_service() -> IRecommendationService:
        """Retorna el servicio de recomendaciones."""
        return RecommendationService()
