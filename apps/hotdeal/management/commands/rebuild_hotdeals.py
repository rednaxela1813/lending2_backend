#apps/hotdeal/management/commands/rebuild_hotdeals.py

from django.core.management.base import BaseCommand
from apps.properties.models import Property
from apps.properties.models.mixins import Availability
from apps.hotdeal.models import HotDealItem
from apps.hotdeal.signals import _default_section



class Command(BaseCommand):
    help = "Rebuild HotDeals from current Property.availability"
    def handle(self, *args, **options):
        section = _default_section()
        # включить свободные
        for p in Property.objects.filter(availability=Availability.AVAILABLE):
            HotDealItem.objects.get_or_create(property=p, defaults={"section": section})
            HotDealItem.objects.filter(property=p).update(is_active=True)
        # выключить не свободные
        HotDealItem.objects.exclude(property__availability=Availability.AVAILABLE).update(is_active=False)
        self.stdout.write(self.style.SUCCESS("HotDeals rebuilt"))
