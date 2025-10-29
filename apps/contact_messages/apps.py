# apps/contact_messages/apps.py
from django.apps import AppConfig

class ContactMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contact_messages"     # <— ВАЖНО: полный путь пакета
    label = "contact_messages"         # стабильный ярлык (не обязателен, но полезен)
    verbose_name = "Contact messages"
