"""
FALTA POR IMPLEMENTAR
Interfaces para el patrón de Dependency Inversion (SOLID)
"""
from abc import ABC, abstractmethod

class IProductRepository(ABC):
    """Interfaz para el repositorio de productos."""
    
    @abstractmethod
    def get_all_products(self):
        """Obtiene todos los productos."""
        pass
    
    @abstractmethod
    def get_product_by_id(self, product_id):
        """Obtiene un producto por ID."""
        pass
    
    @abstractmethod
    def search_products(self, **filters):
        """Busca productos con filtros."""
        pass

class ICurrencyService(ABC):
    """Interfaz para el servicio de conversión de monedas."""
    
    @abstractmethod
    def convert_price(self, price, target_currency):
        """Convierte un precio a la moneda objetivo."""
        pass
    
    @abstractmethod
    def get_exchange_rates(self):
        """Obtiene las tasas de cambio."""
        pass

class IRecommendationService(ABC):
    """Interfaz para el servicio de recomendaciones."""
    
    @abstractmethod
    def get_recommendations(self, user, top_n=3):
        """Obtiene recomendaciones para un usuario."""
        pass
