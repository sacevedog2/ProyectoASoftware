from catalog.models import Producto
from django.db import transaction

with transaction.atomic():
    updated = 0
    for p in Producto.objects.all():
        changed = False
        # Only set if the translated fields are empty or None
        if not getattr(p, 'nombre_es', None):
            p.nombre_es = p.nombre
            changed = True
        if not getattr(p, 'descripcion_es', None):
            p.descripcion_es = p.descripcion
            changed = True
        if changed:
            p.save()
            updated += 1

print(f"Populated translations for {updated} productos.")
