from unittest.mock import patch

from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from django_mercadopago import fixtures
from django_mercadopago import models
from django_mercadopago import views


class CreateNotificationTestCase(TestCase):
    def setUp(self):
        self.account = fixtures.AccountFactory()
        self.preference = fixtures.PreferenceFactory()

    def test_missing_topic(self):
        client = Client()
        response = client.get(
            "/notifications/{}".format(self.preference.reference), {"id": 123}
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_resource_id(self):
        client = Client()
        response = client.get(
            "/notifications/{}".format(self.preference.reference), {"topic": "payment"}
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_topic(self):
        client = Client()
        response = client.get(
            "/notifications/{}".format(self.preference.reference),
            {"topic": "blah", "id": 123},
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_key(self):
        client = Client()
        response = client.get(
            "/notifications/NOSUCHREF", {"topic": "payment", "id": 123}
        )

        self.assertEqual(response.status_code, 404)

    def test_new_notification(self):
        self.assertEqual(models.Notification.objects.count(), 0)

        client = Client()
        response = client.get(
            "/notifications/{}".format(self.preference.reference),
            {"topic": "payment", "id": 123},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Notification.objects.count(), 1)

        notification = models.Notification.objects.first()
        self.assertEqual(notification.topic, models.Notification.TOPIC_PAYMENT)
        self.assertEqual(notification.resource_id, "123")
        self.assertEqual(notification.owner, self.account)
        self.assertEqual(notification.preference, self.preference)
        self.assertEqual(
            notification.status, models.Notification.STATUS_PENDING,
        )

    def test_existing_notification(self):
        models.Notification.objects.create(
            topic=models.Notification.TOPIC_PAYMENT,
            resource_id=123,
            owner=self.account,
            status=models.Notification.STATUS_PROCESSED,
            preference=self.preference,
        )
        self.assertEqual(models.Notification.objects.count(), 1)

        client = Client()
        response = client.get(
            "/notifications/{}".format(self.preference.reference),
            {"topic": "payment", "id": 123},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Notification.objects.count(), 1)
        notification = models.Notification.objects.first()
        self.assertEqual(notification.topic, models.Notification.TOPIC_PAYMENT)
        self.assertEqual(notification.resource_id, "123")
        self.assertEqual(notification.owner, self.account)
        self.assertEqual(notification.preference, self.preference)
        self.assertEqual(
            notification.status, models.Notification.STATUS_PENDING,
        )

    # XXX: Add tests for POST notifications


class PaymentSuccessViewTestCase(TestCase):
    def setUp(self):
        self.preference = fixtures.PreferenceFactory()

    def test_redirect_to_view(self):
        view = views.PaymentSuccessView()
        view.request = RequestFactory().get("/mp/success")
        view.request.GET = {"collection_id": 134783145}

        with patch("django_mercadopago.views.redirect", spec=True,) as mocked_redirect:
            result = view.get(view.request, self.preference.reference)

        self.assertEqual(
            result,
            mocked_redirect("mp_success", pk=models.Notification.objects.last(),),
        )


class PaymentFailureViewTestCase(TestCase):
    def setUp(self):
        self.preference = fixtures.PreferenceFactory()

    def test_redirect_to_view(self):
        view = views.PaymentFailedView()
        view.request = RequestFactory().get("/mp/failure")

        with patch("django_mercadopago.views.redirect", spec=True,) as mocked_redirect:
            result = view.get(view.request, self.preference.reference)

        self.assertEqual(result, mocked_redirect("mp_failure", pk=self.preference.pk,))


class PaymentPendingViewTestCase(TestCase):
    def setUp(self):
        self.preference = fixtures.PreferenceFactory()

    def test_redirect_to_view(self):
        view = views.PaymentPendingView()
        view.request = RequestFactory().get("/mp/pending")

        with patch("django_mercadopago.views.redirect", spec=True,) as mocked_redirect:
            result = view.get(view.request, self.preference.reference)

        self.assertEqual(result, mocked_redirect("mp_pending", pk=self.preference.pk,))
