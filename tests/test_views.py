from django.test import Client, TestCase

from django_mercadopago import fixtures, models


class CreateNotificationTestCase(TestCase):

    def setUp(self):
        self.account = fixtures.AccountFactory()

    def test_missing_topic(self):
        client = Client()
        response = client.get('/notifications/test', {
            'id': 123,
        })

        self.assertEqual(response.status_code, 400)

    def test_missing_resource_id(self):
        client = Client()
        response = client.get('/notifications/test', {
            'topic': 'payment',
        })

        self.assertEqual(response.status_code, 400)

    def test_invalid_topic(self):
        client = Client()
        response = client.get('/notifications/test', {
            'topic': 'blah',
            'id': 123,
        })

        self.assertEqual(response.status_code, 400)

    def test_invalid_slug(self):
        client = Client()
        response = client.get('/notifications/invalid', {
            'topic': 'payment',
            'id': 123,
        })

        self.assertEqual(response.status_code, 404)

    def test_new_notification(self):
        self.assertEqual(models.Notification.objects.count(), 0)

        client = Client()
        response = client.get('/notifications/test', {
            'topic': 'payment',
            'id': 123,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Notification.objects.count(), 1)

        notification = models.Notification.objects.first()
        self.assertEqual(notification.topic, models.Notification.TOPIC_PAYMENT)
        self.assertEqual(notification.resource_id, '123')
        self.assertEqual(notification.owner, self.account)
        self.assertEqual(
            notification.status,
            models.Notification.STATUS_UNPROCESSED,
        )

    def test_existing_notification(self):
        models.Notification.objects.create(
            topic=models.Notification.TOPIC_PAYMENT,
            resource_id=123,
            owner=self.account,
            status=models.Notification.STATUS_PROCESSED,
        )
        self.assertEqual(models.Notification.objects.count(), 1)

        client = Client()
        response = client.get('/notifications/test', {
            'topic': 'payment',
            'id': 123,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Notification.objects.count(), 1)
        notification = models.Notification.objects.first()
        self.assertEqual(notification.topic, models.Notification.TOPIC_PAYMENT)
        self.assertEqual(notification.resource_id, '123')
        self.assertEqual(notification.owner, self.account)
        self.assertEqual(
            notification.status,
            models.Notification.STATUS_UNPROCESSED,
        )
