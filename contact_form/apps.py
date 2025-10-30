from django.apps import AppConfig


class ContactFormConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact_form'
    verbose_name = "Форма обратной связи"
