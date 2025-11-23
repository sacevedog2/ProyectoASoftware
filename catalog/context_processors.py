"""
Context processor para disponibilizar monedas en todos los templates
"""
from catalog.services.currency_service import CurrencyService

def currency_context(request):
    """Agrega información de moneda al contexto de todos los templates."""
    return {
        'current_currency': request.session.get('currency', 'USD'),
        'supported_currencies': CurrencyService.get_supported_currencies(),
        'currency_service': CurrencyService,
    }
