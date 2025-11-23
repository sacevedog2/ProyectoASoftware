# Template tags y filtros para conversión de monedas
from django import template
from catalog.services.currency_service import CurrencyService

register = template.Library()

@register.filter
def convert_currency(price, currency='USD'):
    # Convierte un precio a la moneda especificada.
    if not price:
        return 0
    return CurrencyService.convert_price(price, currency)

@register.filter
def format_price(price, currency='USD'):
    # Formatea un precio con el símbolo de moneda.
    
    if not price:
        return CurrencyService.format_price(0, currency)
    return CurrencyService.format_price(price, currency)

@register.simple_tag
def display_price(price, currency='USD'):
    # Convierte y formatea un precio en un solo paso.
    if not price:
        return CurrencyService.format_price(0, currency)
    
    converted = CurrencyService.convert_price(price, currency)
    return CurrencyService.format_price(converted, currency)

@register.simple_tag
def currency_symbol(currency='USD'):
    # Retorna el símbolo de la moneda.
    return CurrencyService.get_currency_symbol(currency)
