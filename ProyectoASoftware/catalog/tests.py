from django.test import TestCase

from catalog.models import Producto
from catalog.services.service_factory import ServiceFactory


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
