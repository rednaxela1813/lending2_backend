import pytest
from orders.models import LegalAddressOrder
from django.urls import reverse
from rest_framework.test import APIClient



@pytest.mark.django_db
def test_create_legal_address_order():
    order = LegalAddressOrder.objects.create(
        full_name="Ján Novák",
        email="jan.novak@example.com",
        address_choice="Nitra",
        phone="+421900000000",
        note="Chcem začať v júni"
    )
    
    
    assert order.full_name == "Ján Novák"
    assert order.email == "jan.novak@example.com"
    assert order.address_choice == "Nitra"
    assert order.phone == "+421900000000"
    assert order.note == "Chcem začať v júni"
    
    
@pytest.mark.django_db
def test_create_legal_address_order():
    client = APIClient()
    
    payload = {
        "full_name": "Ján Novák 7",
        "email": "jan.novak_7@example.com",
        "company_name": "Firma s.r.o.",
        "phone": "+421900000001",
        "address_choice": "bratislava",  # допустим, два варианта: "nitra" и "bratislava"
        "note": "Chcem vedieť viac o možnostiach doručenia pošty."
    }
    
    url = reverse('legal-address-order')  # замените на ваш URL
    response = client.post(url, data=payload, format='json')
    
    print(response.data)  # добавь перед assert

    assert response.status_code == 201
    assert LegalAddressOrder.objects.count() == 1
    
    order = LegalAddressOrder.objects.first()
    assert order.full_name == payload["full_name"]
    assert order.email == payload["email"]
    assert order.company_name == payload["company_name"]
    assert order.address_choice == payload["address_choice"]
    assert order.note == payload["note"]

    