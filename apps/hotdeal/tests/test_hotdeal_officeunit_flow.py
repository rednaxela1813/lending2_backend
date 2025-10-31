import pytest
from apps.hotdeal.models import HotDealItem, HotDealSection
from apps.properties.models.mixins import Availability

pytestmark = pytest.mark.django_db


def test_hotdeal_created_on_first_available_unit(property_factory, office_unit_factory):
    """
    Когда появляется первый доступный OfficeUnit:
    - Property становится AVAILABLE,
    - создаётся HotDealItem и становится активным.
    """
    p = property_factory(availability=Availability.HIDDEN)
    assert not HotDealItem.objects.filter(property=p).exists()

    office_unit_factory(property=p, availability=Availability.AVAILABLE)

    item = HotDealItem.objects.get(property=p)
    assert item.is_active is True
    assert isinstance(item.section, HotDealSection)


def test_hotdeal_deactivated_when_no_available_units_left(property_factory, office_unit_factory):
    """
    Если не осталось ни одного AVAILABLE юнита, HotDealItem должен деактивироваться.
    """
    p = property_factory()
    u1 = office_unit_factory(property=p, availability=Availability.AVAILABLE)

    item = HotDealItem.objects.get(property=p)
    assert item.is_active is True

    # делаем юнит занятым и убеждаемся, что больше нет доступных
    u1.availability = Availability.OCCUPIED
    u1.save()

    item.refresh_from_db()
    assert item.is_active is False


def test_hotdeal_stays_active_if_any_unit_is_available(property_factory, office_unit_factory):
    """
    Пока существует хотя бы один AVAILABLE юнит, HotDealItem остаётся активным.
    """
    p = property_factory()
    u1 = office_unit_factory(property=p, availability=Availability.AVAILABLE)
    u2 = office_unit_factory(property=p, availability=Availability.RESERVED)

    item = HotDealItem.objects.get(property=p)
    assert item.is_active is True

    # закрываем первый доступный, но добавляем другой доступный — должно остаться активно
    u1.availability = Availability.OCCUPIED
    u1.save()
    office_unit_factory(property=p, availability=Availability.AVAILABLE)

    item.refresh_from_db()
    assert item.is_active is True


def test_hotdeal_deactivates_when_last_unit_deleted(property_factory, office_unit_factory):
    """
    Удаление последнего юнита должно деактивировать HotDealItem.
    """
    p = property_factory()
    u1 = office_unit_factory(property=p, availability=Availability.AVAILABLE)

    item = HotDealItem.objects.get(property=p)
    assert item.is_active is True

    u1.delete()
    item.refresh_from_db()
    assert item.is_active is False


def test_hotdeal_reactivates_when_available_appears_again(property_factory, office_unit_factory):
    """
    После деактивации HotDealItem должен вновь активироваться,
    если снова появился AVAILABLE юнит.
    """
    p = property_factory()
    u1 = office_unit_factory(property=p, availability=Availability.AVAILABLE)
    item = HotDealItem.objects.get(property=p)
    assert item.is_active is True

    # убираем доступность → деактивация
    u1.availability = Availability.OCCUPIED
    u1.save()
    item.refresh_from_db()
    assert item.is_active is False

    # появляется новый доступный юнит → реактивация
    office_unit_factory(property=p, availability=Availability.AVAILABLE)
    item.refresh_from_db()
    assert item.is_active is True


def test_default_section_autocreated(property_factory, office_unit_factory):
    """
    Если активной секции не было, должна создаться дефолтная секция при первом HotDealItem.
    """
    # убеждаемся, что секций нет
    HotDealSection.objects.all().delete()

    p = property_factory()
    office_unit_factory(property=p, availability=Availability.AVAILABLE)

    item = HotDealItem.objects.get(property=p)
    assert item.section is not None
    assert HotDealSection.objects.filter(pk=item.section_id, is_active=True).exists()
