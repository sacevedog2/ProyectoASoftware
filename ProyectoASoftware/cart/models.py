
"""
Autor: Juan Pablo Corena
Fecha: 2025-08-28
Descripción: Modelos CarritoCompra e ItemCarrito para ProyectoASoftware
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class CarritoCompra(models.Model):
    """
    Modelo de carrito de compra.
    Representa los datos y operaciones de un carrito de compra.
    """
    usuario = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE, 
        related_name='carritos', 
        verbose_name=_('Usuario')
    )
    total = models.FloatField(default=0.0, verbose_name=_('Total'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Carrito de compra')
        verbose_name_plural = _('Carritos de compra')

    def __str__(self):
        return f"Carrito de {self.usuario.nombre} - ${self.total}"

    def calcular_total(self):
        """Calcula el total del carrito basado en los items."""
        self.total = sum(item.cantidad * item.producto.precio for item in self.items.all())
        self.save()
        return self.total

    def agregar_producto(self, producto, cantidad=1):
        """Agrega un producto al carrito."""
        # Verificar stock disponible
        item_existente = self.items.filter(producto=producto).first()
        cantidad_actual = item_existente.cantidad if item_existente else 0
        cantidad_total = cantidad_actual + cantidad
        
        if cantidad_total > producto.stock:
            # No permitir agregar más de lo disponible en stock
            return False
        
        item, created = self.items.get_or_create(producto=producto)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
        self.calcular_total()
        return True

    def quitar_producto(self, producto):
        """Quita un producto del carrito."""
        item = self.items.filter(producto=producto).first()
        if item:
            item.delete()
        self.calcular_total()

    @property
    def cantidad_items(self):
        """Retorna la cantidad total de items en el carrito."""
        return sum(item.cantidad for item in self.items.all())


class ItemCarrito(models.Model):
    """
    Modelo de ítem en el carrito de compra.
    Representa los datos y operaciones de un ítem en el carrito.
    """
    carrito = models.ForeignKey(
        CarritoCompra, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name=_('Carrito')
    )
    producto = models.ForeignKey(
        'catalog.Producto', 
        on_delete=models.CASCADE, 
        related_name='items_carrito', 
        verbose_name=_('Producto')
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name=_('Cantidad'))

    class Meta:
        verbose_name = _('Ítem del carrito')
        verbose_name_plural = _('Ítems del carrito')
        unique_together = ['carrito', 'producto']

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"
