"""
Autor: Tu Nombre
Fecha: 2025-08-28
Descripción: Utilidad para generar PDF de facturas.
"""
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generar_factura_pdf(pedido):
    """Genera un PDF de la factura para el pedido dado."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    p.drawString(100, y, f"Factura de Pedido #{pedido.id}")
    y -= 30
    p.drawString(100, y, f"Usuario: {pedido.usuario}")
    y -= 30
    p.drawString(100, y, f"Fecha: {pedido.fecha_pedido}")
    y -= 30
    p.drawString(100, y, f"Estado: {pedido.estado}")
    y -= 30
    p.drawString(100, y, f"Total: ${pedido.total}")
    y -= 50
    p.drawString(100, y, "Detalles del pedido:")
    y -= 30
    # Si existe el modelo DetallePedido y la relación
    detalles = getattr(pedido, 'detalles', None)
    if detalles:
        for detalle in detalles.all():
            p.drawString(120, y, f"Producto: {detalle.producto} | Cantidad: {detalle.cantidad} | Precio Unitario: ${detalle.precio_unitario} | Subtotal: ${detalle.subtotal}")
            y -= 20
            if y < 100:
                p.showPage()
                y = 800
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
