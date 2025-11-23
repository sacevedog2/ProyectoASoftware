from django.core.management.base import BaseCommand
from catalog.models import Producto
from django.db import transaction
import os
import re


def humanize_filename(filename):
    # Remove extension
    name, _ = os.path.splitext(filename)
    # Replace hyphens/underscores with spaces
    name = re.sub(r'[-_]+', ' ', name)
    # Remove common prefixes like 'IMG', 'DSC', trailing numbers
    name = re.sub(r'^(IMG|DSC|photo)\s*', '', name, flags=re.IGNORECASE)
    # Remove digits groups
    name = re.sub(r'\b\d+\b', '', name)
    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()
    # Title case
    name = name.title()
    return name


class Command(BaseCommand):
    help = 'Infer product nombre_es from producto.imagen filename when translation is missing.'

    def handle(self, *args, **options):
        products = Producto.objects.all()
        total = products.count()
        updated = 0
        samples = []
        with transaction.atomic():
            for p in products:
                # collect sample before
                samples.append((p.id, p.imagen.name if p.imagen else None, p.nombre, p.nombre_es))
                if (not getattr(p, 'nombre_es', None) or getattr(p, 'nombre_es', '').strip() == '') and p.imagen:
                    filename = os.path.basename(p.imagen.name)
                    inferred = humanize_filename(filename)
                    if inferred:
                        p.nombre_es = inferred
                        # Optionally set descripcion_es if empty
                        if not getattr(p, 'descripcion_es', None):
                            p.descripcion_es = inferred
                        p.save()
                        updated += 1
        self.stdout.write(self.style.SUCCESS(f'Total products: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Updated nombre_es for {updated} products.'))
        self.stdout.write('Sample before (id, imagen_name, nombre, nombre_es):')
        for s in samples[:10]:
            self.stdout.write(str(s))
