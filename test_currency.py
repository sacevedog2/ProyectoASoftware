""" Script de prueba para el servicio de conversión de monedas
Ejecutar: python manage.py shell < test_currency.py """

from catalog.services.currency_service import CurrencyService

print("=" * 60)
print(" PRUEBA DEL SISTEMA DE CONVERSIÓN DE MONEDAS")
print("=" * 60)

# Test 1: Obtener tasas de cambio
print("\n1 Obteniendo tasas de cambio...")
tasas = CurrencyService.get_exchange_rates()
print(f" Tasas obtenidas: {len(tasas)} monedas disponibles")
print(f"   USD → COP: {tasas.get('COP', 'N/A')}")
print(f"   USD → EUR: {tasas.get('EUR', 'N/A')}")
print(f"   USD → MXN: {tasas.get('MXN', 'N/A')}")

# Test 2: Conversión de precios
print("\n2️⃣ Probando conversión de precios...")
precio_usd = 100.00
monedas_test = ['USD', 'COP', 'EUR', 'GBP', 'MXN']

for moneda in monedas_test:
    convertido = CurrencyService.convert_price(precio_usd, moneda)
    formateado = CurrencyService.format_price(convertido, moneda)
    print(f"   ${precio_usd} USD → {formateado}")

# Test 3: Monedas soportadas
print("\n3️⃣ Monedas soportadas en el sistema...")
soportadas = CurrencyService.get_supported_currencies()
for codigo, info in soportadas.items():
    print(f"   {codigo}: {info['symbol']} {info['name']}")

# Test 4: Símbolos de moneda
print("\n4️⃣ Símbolos de moneda...")
for codigo in ['USD', 'EUR', 'COP', 'GBP']:
    simbolo = CurrencyService.get_currency_symbol(codigo)
    print(f"   {codigo} → {simbolo}")

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 60)
