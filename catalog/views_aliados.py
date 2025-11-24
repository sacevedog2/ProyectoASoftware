"""
Vistas para consumir el servicio del equipo aliado (equipo precedente).

La URL del servicio aliado se configura mediante la variable de entorno
``ALIADOS_API_URL``. El servicio debe devolver un JSON con una lista de
productos o un objeto que contenga una clave "productos".
"""
import os
import requests

from django.views.generic import TemplateView


class ProductosAliadosView(TemplateView):
    """
    Consume el servicio del equipo aliado y muestra sus productos en una tabla.
    """
    template_name = "catalog/productos_aliados.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        api_url = os.getenv("ALIADOS_API_URL", "").strip()
        context["api_url"] = api_url
        context["productos_aliados"] = []
        context["error_aliados"] = None

        if not api_url:
            context["error_aliados"] = (
                "No se ha configurado la variable de entorno ALIADOS_API_URL "
                "con la URL del servicio del equipo aliado."
            )
            return context

        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Formatos permitidos: lista directa o dict con clave productos/results
            if isinstance(data, dict):
                productos_crudos = data.get("productos", data.get("results", []))
            else:
                productos_crudos = data

            productos_normalizados = []
            for item in productos_crudos:
                # Usar exactamente los campos del aliado; si alguno falta, poner None
                productos_normalizados.append({
                    'idProducto': item.get('idProducto'),
                    'nombreProducto': item.get('nombreProducto'),
                    'tipoProducto': item.get('tipoProducto'),
                    'marcaProducto': item.get('marcaProducto'),
                    'cantidadDeProducto': item.get('cantidadDeProducto'),
                    'fechaVencimientoProducto': item.get('fechaVencimientoProducto'),
                    'precioDeProducto': item.get('precioDeProducto'),
                    'imagenProducto': item.get('imagenProducto'),
                })

            context["productos_aliados"] = productos_normalizados
        except Exception as exc:  # noqa: BLE001
            context["error_aliados"] = f"Error al consumir el servicio aliado: {exc}"
            context["productos_aliados"] = []

        return context
