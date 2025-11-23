""""Autor: David Restrepo"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Pago(models.Model):
    """
    Modelo para los pagos realizados por los usuarios.
    """
    
    METODO_CHOICES = [
        ('contraentrega', 'Pago contra entrega'),
        ('tarjeta', 'Pago con tarjeta'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]
    
    pedido = models.ForeignKey(
        'orders.Pedido', 
        on_delete=models.CASCADE, 
        related_name='pagos'
    )
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(
        max_length=30, 
        choices=METODO_CHOICES,
        default='contraentrega'
    )
    monto = models.FloatField(default=0.0)
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    direccion_entrega = models.TextField(blank=True, null=True)
    tarjeta_usada = models.ForeignKey(
        'users.Tarjeta',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pagos_realizados'
    )

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago {self.pk} - {self.get_metodo_display()} - ${self.monto}"

    def procesar_pago(self):
        """Simula el procesamiento del pago."""
        if self.metodo == 'contraentrega':
            self.estado = 'completado'
        else:  # tarjeta
            # Simulación: 90% de éxito
            import random
            if random.random() < 0.9:
                self.estado = 'completado'
            else:
                self.estado = 'fallido'
        self.save()
        return self.estado == 'completado'
