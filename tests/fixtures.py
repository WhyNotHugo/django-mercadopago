from factory.django import DjangoModelFactory

from django_mercadopago import models


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = models.Account
        django_get_or_create = ('name',)

    name = 'Test account'
    slug = 'test'
    app_id = 'f9S92sb1cPMUbJqfpLIrw1q6'
    secret_key = 'f9S92sb1cPMUbJqfpLIrw1q6'
    sandbox = True
