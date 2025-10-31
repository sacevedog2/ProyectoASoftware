"""
Middleware para gestión de moneda en sesión
"""

class CurrencyMiddleware:
    """Middleware que asegura que la moneda esté configurada en la sesión."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Establecer moneda por defecto si no existe
        if 'currency' not in request.session:
            request.session['currency'] = 'USD'
        
        response = self.get_response(request)
        return response
