import json

import pytest
import responses

from django_mercadopago import fixtures
from django_mercadopago import models


preference_response = {
    "processing_modes": [],
    "metadata": {},
    "binary_mode": False,
    "payment_methods": {
        "excluded_payment_methods": [{"id": ""}],
        "excluded_payment_types": [{"id": ""}],
        "installments": None,
        "default_payment_method_id": None,
        "default_installments": None,
    },
    "collector_id": 152658942,
    "operation_type": "regular_payment",
    "items": [
        {
            "id": "",
            "picture_url": "",
            "title": "Test",
            "description": "A nice, high quality product.",
            "category_id": "services",
            "currency_id": "ARS",
            "quantity": 1,
            "unit_price": 120,
        }
    ],
    "payer": {
        "name": "",
        "surname": "",
        "email": "",
        "date_created": "",
        "phone": {"area_code": "", "number": ""},
        "identification": {"type": "", "number": ""},
        "address": {"street_name": "", "street_number": None, "zip_code": ""},
    },
    "back_urls": {
        "success": "http://localhost:8001/post_payment/ref-123",
        "pending": "http://localhost:8001/payment_pending/ref-123",
        "failure": "http://localhost:8001/payment_failed/ref-123",
    },
    "auto_return": "all",
    "client_id": "3641931198760523",
    "marketplace": "NONE",
    "marketplace_fee": 0,
    "shipments": {
        "receiver_address": {
            "zip_code": "",
            "street_number": None,
            "street_name": "",
            "floor": "",
            "apartment": "",
        }
    },
    "notification_url": "http://localhost:8001/notifications/ref-123",
    "external_reference": "ref-123",
    "additional_info": "",
    "expires": False,
    "expiration_date_from": None,
    "expiration_date_to": None,
    "date_created": "2019-10-13T15:39:08.981-04:00",
    "id": "152658942-f090626e-6d4d-4877-a3d5-292e8877e4cb",
    "init_point": "https://www.mercadopago.com/init_point",
    "sandbox_init_point": "https://sbox.mercadopago.com/init_point",
}


@pytest.mark.django_db
@responses.activate
def test_preference_request():
    """Preference creation runs the expected query."""
    responses.add(
        responses.POST,
        "https://api.mercadopago.com/oauth/token",
        json={
            "access_token": "APP_USR-3641931198760523",
            "refresh_token": "TG-5da379a4705f640006b69d70-152658942",
            "live_mode": True,
            "user_id": 152658949,
            "token_type": "bearer",
            "expires_in": 21600,
            "scope": "offline_access read write",
        },
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.mercadopago.com/checkout/preferences",
        json=preference_response,
        status=200,
    )

    preference = fixtures.PreferenceFactory(mp_id=None, reference="ref-123",)
    fixtures.ItemFactory(preference=preference, title="Test")
    preference.submit()

    expected_url = (
        "https://api.mercadopago.com/checkout/preferences?access_token="
        "APP_USR-3641931198760523"
    )
    expected_request = {
        "auto_return": "all",
        "items": [
            {
                "title": "Test",
                "currency_id": "ARS",
                "description": "A nice, high quality product.",
                "category_id": "services",
                "quantity": 1,
                "unit_price": 120.0,
            }
        ],
        "external_reference": "ref-123",
        "back_urls": {
            "success": "http://localhost:8001/post_payment/ref-123",
            "pending": "http://localhost:8001/payment_pending/ref-123",
            "failure": "http://localhost:8001/payment_failed/ref-123",
        },
        "notification_url": "http://localhost:8001/notifications/ref-123",
    }

    assert len(responses.calls) == 2
    assert responses.calls[1].request.url == expected_url
    assert json.loads(responses.calls[1].request.body) == expected_request


@pytest.mark.django_db
@responses.activate
def test_preference_creation():
    """Preference creation assigned attributes properly."""
    responses.add(
        responses.POST,
        "https://api.mercadopago.com/oauth/token",
        json={
            "access_token": "APP_USR-3641931198760523",
            "refresh_token": "TG-5da379a4705f640006b69d70-152658942",
            "live_mode": True,
            "user_id": 152658949,
            "token_type": "bearer",
            "expires_in": 21600,
            "scope": "offline_access read write",
        },
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.mercadopago.com/checkout/preferences",
        json=preference_response,
        status=200,
    )

    preference = fixtures.PreferenceFactory(mp_id=None, reference="ref-123",)
    fixtures.ItemFactory(preference=preference, title="Test")
    preference.submit()

    assert preference.items.first().title == "Test"
    assert preference.items.first().unit_price == 120
    assert preference.items.first().quantity == 1
    assert preference.mp_id == "152658942-f090626e-6d4d-4877-a3d5-292e8877e4cb"
    assert preference.payment_url == "https://www.mercadopago.com/init_point"
    assert preference.sandbox_url == "https://sbox.mercadopago.com/init_point"
    assert preference.reference == "ref-123"
    assert isinstance(preference.owner, models.Account)
