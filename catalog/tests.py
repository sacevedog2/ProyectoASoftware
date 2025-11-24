from django.test import TestCase

from catalog.models import Producto
from catalog.services.service_factory import ServiceFactory
from django.urls import reverse
from django.test import Client
from unittest.mock import patch, Mock


class ProductoModelTest(TestCase):
    """Pruebas unitarias simples para el modelo Producto."""

    def test_crear_producto(self):
        producto = Producto.objects.create(
            nombre="Camiseta de prueba",
            descripcion="Una camiseta para pruebas unitarias",
            precio=19990,
            stock=10,
            talla="S,M",
            color="Negro",
            tipo="camiseta",
            genero="hombre",
        )
        self.assertEqual(str(producto.nombre), "Camiseta de prueba")
        self.assertGreaterEqual(producto.stock, 0)


class ServiceFactoryTest(TestCase):
    """Pruebas para demostrar el uso de la Inversión de Dependencias."""

    def test_obtener_repositorio_productos(self):
        repo = ServiceFactory.get_product_repository()
        # Debe exponer los métodos definidos en la interfaz
        self.assertTrue(hasattr(repo, "get_all_products"))
        self.assertTrue(callable(repo.get_all_products))

    def test_obtener_servicio_recomendaciones(self):
        service = ServiceFactory.get_recommendation_service()
        self.assertTrue(hasattr(service, "get_recommendations"))
        self.assertTrue(callable(service.get_recommendations))


class ProductoAPITest(TestCase):
    """Prueba del endpoint plano /api/productos/."""

    def setUp(self):
        self.client = Client()
        Producto.objects.create(
            nombre="Camiseta Stock",
            descripcion="Camiseta con stock",
            precio=10000,
            stock=5,
            talla="M,L",
            color="Azul",
            tipo="camiseta",
            genero="hombre",
        )
        Producto.objects.create(
            nombre="Buzo Sin Stock",
            descripcion="Buzo sin stock",
            precio=20000,
            stock=0,
            talla="S",
            color="Rojo",
            tipo="buzo",
            genero="mujer",
        )

    def test_listado_plano_campos_aliados(self):
        url = reverse('api:producto_listado_plano')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)
        first = data[0]
        for campo in ['idProducto','nombreProducto','tipoProducto','marcaProducto','cantidadDeProducto','precioDeProducto']:
            self.assertIn(campo, first)


class ProductosAliadosViewTest(TestCase):
    """Prueba de normalización de datos aliados."""

    def setUp(self):
        self.client = Client()

    @patch('catalog.views_aliados.requests.get')
    def test_consumo_aliado_normaliza_campos(self, mock_get):
        # Preparar respuesta simulada
        fake_json = [
            {
                'idProducto': 8,
                'nombreProducto': 'Aceite de Masaje Anticelulitis',
                'tipoProducto': 'Aceite',
                'marcaProducto': 'La Roche-Posay',
                'cantidadDeProducto': 1,
                'fechaVencimientoProducto': '2026-09-23',
                'precioDeProducto': 100000,
                'imagenProducto': 'http://localhost:8000/media/productos/R.jpeg'
            }
        ]
        mock_resp = Mock()
        mock_resp.json.return_value = fake_json
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        with patch.dict('os.environ', {'ALIADOS_API_URL': 'http://aliado.test/api'}):
            resp = self.client.get(reverse('catalog:productos_aliados'))
            self.assertEqual(resp.status_code, 200)
            # La plantilla debería contener el nombreProducto
            self.assertContains(resp, 'Aceite de Masaje Anticelulitis')
            self.assertContains(resp, 'La Roche-Posay')

