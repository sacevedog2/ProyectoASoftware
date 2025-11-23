"""  Vista para cambiar la moneda del usuario """
from django.http import JsonResponse
from django.views import View
from catalog.services.currency_service import CurrencyService

class CambiarMonedaView(View):
    # Vista para cambiar la moneda preferida del usuario.
    
    def post(self, request):
        # Cambia la moneda en la sesión del usuario.
        currency = request.POST.get('currency', 'USD')
        
        # Validar que la moneda sea soportada
        if currency not in CurrencyService.get_supported_currencies():
            return JsonResponse({
                'success': False,
                'message': 'Moneda no soportada'
            }, status=400)
        
        # Guardar en sesión
        request.session['currency'] = currency
        
        return JsonResponse({
            'success': True,
            'currency': currency,
            'symbol': CurrencyService.get_currency_symbol(currency),
            'message': f'Moneda cambiada a {currency}'
        })
