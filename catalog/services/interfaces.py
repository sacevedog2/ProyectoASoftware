"""
Interfaces para el patrón de Dependency Inversion (SOLID).

Estas interfaces definen contratos que pueden ser implementados por
distintas clases concretas (por ejemplo, repositorios basados en Django ORM,
servicios que llaman APIs externas, etc.).
De esta forma, las vistas y la lógica de negocio dependen de abstracciones
y no de implementaciones concretas.
"""
from abc import ABC, abstractmethod


class IProductRepository(ABC):
    """Interfaz para el repositorio de productos."""

    @abstractmethod
    def get_all_products(self):
        """Obtiene todos los productos."""
        raise NotImplementedError

    @abstractmethod
    def get_product_by_id(self, product_id):
        """Obtiene un producto por su ID o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def get_top_selling_products(self, top_n: int = 3):
        """Obtiene los productos más vendidos."""
        raise NotImplementedError


class ICurrencyService(ABC):
    """Interfaz para un servicio de conversión de monedas."""

    @abstractmethod
    def convert_price(self, price: float, target_currency: str) -> float:
        """Convierte un precio a otra moneda."""
        raise NotImplementedError

    @abstractmethod
    def get_supported_currencies(self):
        """Retorna la lista de monedas soportadas."""
        raise NotImplementedError

    @abstractmethod
    def get_exchange_rates(self):
        """Obtiene las tasas de cambio."""
        raise NotImplementedError


class IRecommendationService(ABC):
    """Interfaz para el servicio de recomendaciones."""

    @abstractmethod
    def get_recommendations(self, user, top_n: int = 3):
        """Obtiene recomendaciones para un usuario."""
        raise NotImplementedError
