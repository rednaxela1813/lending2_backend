from apps.properties.models.mixins import Availability

def compute_property_availability_from_units(property_obj) -> str:
    """
    Возвращает агрегированный статус для Property на основе связанных OfficeUnit.
    Правило:
      - если есть хотя бы один OfficeUnit со статусом AVAILABLE → Property.AVAILABLE
      - иначе, если есть хотя бы один OfficeUnit со статусом RESERVED → Property.RESERVED
      - иначе → Property.OCCUPIED
    (Можно адаптировать под твою бизнес-логику)
    """
    units = property_obj.office_units.all().only("availability")
    any_available = any(u.availability == Availability.AVAILABLE for u in units)
    if any_available:
        return Availability.AVAILABLE
    any_reserved = any(u.availability == Availability.RESERVED for u in units)
    if any_reserved:
        return Availability.RESERVED
    return Availability.OCCUPIED

