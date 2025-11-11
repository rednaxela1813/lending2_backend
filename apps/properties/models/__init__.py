# обязательно: чтобы Django «увидел» все модели при импорте приложения
from .mixins import Availability, AvailabilityMixin, AvailabilityManager, AvailabilityQuerySet

from .property import *
from .office import *
from .billboard import *
from .legal_address import *
# from .hotdeals_link import ...  # если будет

__all__ = [
    "Availability", "AvailabilityMixin", "AvailabilityManager", "AvailabilityQuerySet",
    "Property", "PropertyImage", "PropertyType",
    "OfficeUnit", "OfficeUnitImage",
    
]
