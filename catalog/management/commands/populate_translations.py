from django.core.management.base import BaseCommand
from catalog.models import Producto
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate nombre_es and descripcion_es from existing nombre and descripcion'

    def handle(self, *args, **options):
        with transaction.atomic():
            updated = 0
            for p in Producto.objects.all():
                changed = False
                if not getattr(p, 'nombre_es', None):
                    p.nombre_es = p.nombre
                    changed = True
                if not getattr(p, 'descripcion_es', None):
                    p.descripcion_es = p.descripcion
                    changed = True
                if changed:
                    p.save()
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f'Populated translations for {updated} productos.'))
