from django.core.management.base import BaseCommand
from catalog.models import Producto
from django.db import transaction

class Command(BaseCommand):
    help = 'Restore producto.nombre and producto.descripcion from nombre_es/descripcion_es when originals are empty.'

    def handle(self, *args, **options):
        products = Producto.objects.all()
        total = products.count()
        restored = 0
        samples = []
        with transaction.atomic():
            for p in products:
                before_nombre = p.nombre
                before_descripcion = p.descripcion
                changed = False
                # Only restore when original field empty or null
                if (not p.nombre or str(p.nombre).strip() == '') and getattr(p, 'nombre_es', None):
                    p.nombre = p.nombre_es
                    changed = True
                if (not p.descripcion or str(p.descripcion).strip() == '') and getattr(p, 'descripcion_es', None):
                    p.descripcion = p.descripcion_es
                    changed = True
                if changed:
                    p.save()
                    restored += 1
                samples.append((p.id, before_nombre, p.nombre, before_descripcion, p.descripcion))

        self.stdout.write(self.style.SUCCESS(f'Total products: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Restored fields for {restored} products.'))
        self.stdout.write('Samples (id, nombre_before, nombre_after, descripcion_before, descripcion_after):')
        for s in samples[:20]:
            self.stdout.write(str(s))
