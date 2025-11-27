# apps/company/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CompanyInfo, FooterInfo


@receiver(post_save, sender=CompanyInfo)
def create_or_update_footerinfo(sender, instance: CompanyInfo, created, **kwargs):
    """
    При создании/сохранении CompanyInfo:
    - создаём FooterInfo, если его ещё нет;
    - заполняем поля контактных данных, если они пустые.
    """
    footer, footer_created = FooterInfo.objects.get_or_create(company=instance)

    # Заполняем только те поля, которые ещё не заданы вручную
    if not footer.contact_email:
        footer.contact_email = instance.email

    if not footer.contact_phone:
        footer.contact_phone = instance.phone

    if not footer.contact_address:
        footer.contact_address = instance.address

    # Можно также автозаполнить about_title, если хочешь:
    if not footer.about_title:
        footer.about_title = instance.name

    footer.save()
