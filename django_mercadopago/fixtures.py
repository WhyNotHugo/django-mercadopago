from datetime import datetime

from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from django_mercadopago import models


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = models.Account
        django_get_or_create = ('name',)

    name = 'Test account'
    slug = 'test'
    app_id = 'zWFmI1iAcw0mwEqf'
    secret_key = '3NjwHgyWcIDisf7MYk1UgWSTFe47DBwe'
    sandbox = True


class PreferenceFactory(DjangoModelFactory):
    class Meta:
        model = models.Preference

    owner = SubFactory(AccountFactory)
    # mp_id = Sequence(lambda n: '2hLhPNlP3DJvMW48dAYn%d' % n)
    payment_url = 'http://localhost/post_payment'
    sandbox_url = 'http://localhost:8000/post_payment'
    reference = Sequence(lambda n: 'REF_%d' % n)


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = models.Item

    preference = SubFactory(PreferenceFactory)
    title = Sequence(lambda n: 'item_%d' % n)
    description = Sequence(lambda n: 'item_description_%d' % n)
    unit_price = 10.0


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = models.Payment

    preference = SubFactory(PreferenceFactory)
    mp_id = 1234
    created = datetime(2017, 6, 12)
    approved = datetime(2017, 6, 13)


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = models.Notification

    owner = SubFactory(AccountFactory)
    status = models.Notification.STATUS_PENDING
    topic = models.Notification.TOPIC_PAYMENT
    resource_id = Sequence(lambda n: 1234 + n)
