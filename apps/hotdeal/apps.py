# apps/hotdeal/apps.py
from django.apps import AppConfig


class HotdealsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hotdeal'
    label = 'hotdeal'
    
    def ready(self):
        from . import signals  # noqa: F401  (чтобы сигналы загрузились)
    
    
