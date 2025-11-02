from django.core.management.base import BaseCommand
from dashboard.models import SiteSection, SiteSlot

SECTIONS = [
    ('home','Homepage'),
    ('services','Services'),
    ('footer','Footer'),
]

SLOTS = [
    ('home','hero_title','Hero title','text'),
    ('home','hero_lead','Hero lead','text'),
    ('home','hero_image','Hero image','image'),
    ('services','headline','Block headline','text'),
    ('footer','about','Footer about','text'),
    ('footer','logo','Footer logo','image'),
]

class Command(BaseCommand):
    help = "Seed dashboard sections/slots"

    def handle(self, *args, **kwargs):
        for slug, name in SECTIONS:
            SiteSection.objects.get_or_create(slug=slug, defaults={'name':name})
        for s_slug, slot_slug, name, kind in SLOTS:
            section = SiteSection.objects.get(slug=s_slug)
            SiteSlot.objects.get_or_create(section=section, slug=slot_slug,
                                           defaults={'name':name,'kind':kind})
        self.stdout.write(self.style.SUCCESS('Sections/slots seeded'))

