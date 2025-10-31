"""
Factory para crear instancias de servicios (patrón Factory)
"""
from catalog.services.currency_service import CurrencyService
from catalog.services.recommendations import productos_recomendados
from catalog.services.ranking import productos_mas_vendidos

class ServiceFactory:
    """Factory para crear instancias de servicios."""
    
    @staticmethod
    def get_currency_service():
        """Retorna una instancia del servicio de monedas."""
        return CurrencyService
    
    @staticmethod
    def get_recommendation_service():
        """Retorna el servicio de recomendaciones."""
        return productos_recomendados
    
    @staticmethod
    def get_ranking_service():
        """Retorna el servicio de ranking."""
        return productos_mas_vendidos
