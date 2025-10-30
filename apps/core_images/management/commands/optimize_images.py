from django.core.management.base import BaseCommand
from django.apps import apps
from apps.core_images.mixins import ImageOptimizationMixin


class Command(BaseCommand):
    help = "Оптимизировать изображения у всех моделей, использующих ImageOptimizationMixin"

    def handle(self, *args, **options):
        total, changed = 0, 0
        for model in apps.get_models():
            if not issubclass(model, ImageOptimizationMixin):
                continue
            qs = model.objects.all()
            for obj in qs.iterator():
                total += 1
                before = obj.__class__.objects.filter(pk=obj.pk).values().first()
                # save() триггерит оптимизацию (save=False внутри f.save())
                obj.save()
                changed += 1
        self.stdout.write(self.style.SUCCESS(f"Processed: {total}, saved: {changed}"))
