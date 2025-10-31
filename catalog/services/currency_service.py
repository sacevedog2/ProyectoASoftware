"""
Servicio de conversión de monedas usando API externa
"""
import requests
from decimal import Decimal

class CurrencyService:
    """Servicio para obtener tasas de cambio y convertir monedas."""
    
    # API pública gratuita para tasas de cambio
    API_URL = "https://api.exchangerate-api.com/v4/latest/"
    BASE_CURRENCY = "COP"  # Peso colombiano como base
    
    # Cache de tasas de cambio (en producción usar Redis o similar)
    _rates_cache = {}
    
    @classmethod
    def get_supported_currencies(cls):
        """Retorna las monedas soportadas con su información."""
        return {
            'USD': {'name': 'Dólar Americano', 'symbol': '$'},
            'EUR': {'name': 'Euro', 'symbol': '€'},
            'GBP': {'name': 'Libra Esterlina', 'symbol': '£'},
            'COP': {'name': 'Peso Colombiano', 'symbol': '$'},
            'MXN': {'name': 'Peso Mexicano', 'symbol': '$'},
            'ARS': {'name': 'Peso Argentino', 'symbol': '$'},
            'CLP': {'name': 'Peso Chileno', 'symbol': '$'},
            'BRL': {'name': 'Real Brasileño', 'symbol': 'R$'},
        }
    
    @classmethod
    def get_currency_symbol(cls, currency):
        """Retorna el símbolo de la moneda."""
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'COP': '$',
            'MXN': '$',
            'ARS': '$',
            'CLP': '$',
            'BRL': 'R$',
        }
        return symbols.get(currency, currency)
    
    @classmethod
    def get_exchange_rates(cls):
        """Obtiene las tasas de cambio desde la API."""
        try:
            response = requests.get(f"{cls.API_URL}{cls.BASE_CURRENCY}", timeout=5)
            response.raise_for_status()
            data = response.json()
            cls._rates_cache = data.get('rates', {})
            return cls._rates_cache
        except Exception as e:
            print(f"Error obteniendo tasas de cambio: {e}")
            # Tasas de respaldo en caso de error de API
            return {
                'USD': 0.00025,
                'EUR': 0.00023,
                'GBP': 0.00020,
                'COP': 1.0,
                'MXN': 0.0045,
                'ARS': 0.25,
                'CLP': 0.23,
                'BRL': 0.0013,
            }
    
    @classmethod
    def convert_price(cls, price, target_currency):
        """Convierte un precio de COP a la moneda objetivo."""
        if target_currency == cls.BASE_CURRENCY:
            return price
        
        rates = cls._rates_cache if cls._rates_cache else cls.get_exchange_rates()
        rate = rates.get(target_currency, 1.0)
        
        converted = Decimal(str(price)) * Decimal(str(rate))
        return float(converted)
    
    @classmethod
    def format_price(cls, price, currency):
        """Formatea un precio con el símbolo de moneda."""
        symbol = cls.get_currency_symbol(currency)
        return f"{symbol}{price:,.2f}"
