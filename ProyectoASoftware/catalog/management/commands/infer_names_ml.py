from django.core.management.base import BaseCommand
from catalog.models import Producto
from django.conf import settings
from PIL import Image
import os
import re

# We'll import torch/torchvision lazily so Django can still start if they're missing
try:
    import torch
    from torchvision import models, transforms
except Exception:
    torch = None
    models = None
    transforms = None


def map_label_to_spanish(label):
    # Lowercase for checks
    s = label.lower()
    # Heuristic mappings
    if any(k in s for k in ['t-shirt', 'tshirt', 'jersey', 'tee']):
        return 'Camiseta'
    if any(k in s for k in ['shirt']):
        return 'Camisa'
    if any(k in s for k in ['jean', 'denim', 'jeans']):
        return 'Pantalón vaquero'
    if any(k in s for k in ['trouser', 'pants', 'chino', 'slacks']):
        return 'Pantalón'
    if any(k in s for k in ['shorts']):
        return 'Shorts'
    if any(k in s for k in ['sweatshirt', 'hoodie', 'sweater', 'jumper', 'pullover']):
        return 'Buzo'
    if any(k in s for k in ['coat', 'jacket']):
        return 'Chaqueta'
    if any(k in s for k in ['dress']):
        return 'Vestido'
    if any(k in s for k in ['skirt']):
        return 'Falda'
    if any(k in s for k in ['shoe', 'sneaker', 'boot', 'loafer']):
        return 'Zapatos'
    if any(k in s for k in ['sock']):
        return 'Calcetines'
    if any(k in s for k in ['bag', 'backpack', 'rucksack']):
        return 'Bolso'
    if any(k in s for k in ['hat', 'cap', 'beret']):
        return 'Gorra'
    # fallback: title case the english label
    return label.title()


class Command(BaseCommand):
    help = 'Infer product names using a pretrained ImageNet model. By default runs in dry-run (no DB write). Use --commit to save.'

    def add_arguments(self, parser):
        parser.add_argument('--commit', action='store_true', help='Save inferred names to the DB')
        parser.add_argument('--topk', type=int, default=1, help='How many top predictions to show')

    def handle(self, *args, **options):
        commit = options['commit']
        topk = options['topk']

        if torch is None:
            self.stderr.write('PyTorch/torchvision not available. Please install torch and torchvision to use this command.')
            return

        # Prepare model and transforms
        device = torch.device('cpu')
        # Use a lightweight ResNet50 pre-trained weight
        try:
            weights = models.ResNet50_Weights.DEFAULT
            model = models.resnet50(weights=weights)
            preprocess = weights.transforms()
        except Exception:
            # Fallback for older torchvision versions
            model = models.resnet50(pretrained=True)
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),
            ])

        model.to(device)
        model.eval()

        # Get labels
        try:
            labels = weights.meta['categories']
        except Exception:
            # Try from local file or fallback
            labels = None

        products = Producto.objects.all()
        total = products.count()
        updated = 0
        samples = []

        for p in products:
            img_field = p.imagen
            if not img_field:
                samples.append((p.id, None, p.nombre_es, None))
                continue
            img_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
            if not os.path.exists(img_path):
                samples.append((p.id, img_field.name, p.nombre_es, 'IMAGE_NOT_FOUND'))
                continue

            try:
                img = Image.open(img_path).convert('RGB')
            except Exception as e:
                samples.append((p.id, img_field.name, p.nombre_es, f'ERROR_OPEN:{e}'))
                continue

            input_tensor = preprocess(img).unsqueeze(0).to(device)
            with torch.no_grad():
                outputs = model(input_tensor)
                probs = torch.nn.functional.softmax(outputs[0], dim=0)
                topk_probs, topk_idxs = torch.topk(probs, k=topk)

            preds = []
            for prob, idx in zip(topk_probs.tolist(), topk_idxs.tolist()):
                if labels and 0 <= idx < len(labels):
                    label = labels[idx]
                else:
                    label = f'Class-{idx}'
                preds.append((label, prob))

            # Map best label to spanish
            best_label = preds[0][0]
            inferred = map_label_to_spanish(best_label)

            samples.append((p.id, img_field.name, p.nombre_es, inferred))

            if commit and (not getattr(p, 'nombre_es', None) or getattr(p, 'nombre_es','').strip() == ''):
                p.nombre_es = inferred
                if not getattr(p, 'descripcion_es', None) or getattr(p, 'descripcion_es','').strip() == '':
                    p.descripcion_es = inferred
                p.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Total products scanned: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Updated nombre_es for {updated} products.'))
        self.stdout.write('Samples (id, imagen_name, nombre_es_before, inferred):')
        for s in samples[:20]:
            self.stdout.write(str(s))
