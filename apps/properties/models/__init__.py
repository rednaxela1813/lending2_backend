# обязательно: чтобы Django «увидел» все модели при импорте приложения
from .mixins import Availability, AvailabilityMixin, AvailabilityManager, AvailabilityQuerySet

from .property import Property, PropertyImage, PropertyType
from .office import OfficeUnit, OfficeUnitImage
# from .billboard import Billboard
# from .legal_address import LegalAddress
# from .hotdeals_link import ...  # если будет

__all__ = [
    "Availability", "AvailabilityMixin", "AvailabilityManager", "AvailabilityQuerySet",
    "Property", "PropertyImage", "PropertyType",
    "OfficeUnit", "OfficeUnitImage",
    
]
