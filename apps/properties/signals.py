from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.properties.models.office import OfficeUnit
from apps.properties.models.property import Property
from apps.properties.utils import compute_property_availability_from_units
from apps.properties.models.mixins import Availability


def _recalc_and_save_property(property_obj: Property):
    new_status = compute_property_availability_from_units(property_obj)
    if property_obj.availability != new_status:
        property_obj.availability = new_status
        property_obj.save(update_fields=["availability"])

@receiver(post_save, sender=OfficeUnit)
def on_officeunit_change(sender, instance: OfficeUnit, **kwargs):
    _recalc_and_save_property(instance.property)

@receiver(post_delete, sender=OfficeUnit)
def on_officeunit_delete(sender, instance: OfficeUnit, **kwargs):
    _recalc_and_save_property(instance.property)
