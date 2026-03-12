# apps/properties/models/mixins.py
from django.db import models
from django.utils.translation import gettext_lazy as _



class Availability(models.TextChoices):
    AVAILABLE = "available", _("Volné")
    RESERVED  = "reserved",  _("Rezervováno")
    OCCUPIED  = "occupied",  _("Obsazeno")
    HIDDEN    = "hidden",    _("Skryto/na servisu")
    
    
class AvailabilityQuerySet(models.QuerySet):
    def available(self):
        return self.filter(availability=Availability.AVAILABLE)
    

class AvailabilityManager(models.Manager.from_queryset(AvailabilityQuerySet)):
    pass



class AvailabilityMixin(models.Model):
    availability = models.CharField(
        max_length=16,
        choices=Availability.choices,
        default=Availability.AVAILABLE,
        db_index=True,
    )

    objects = AvailabilityManager()

    class Meta:
        abstract = True