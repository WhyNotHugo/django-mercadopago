from django.conf import settings
from django.db import models
from mercadopago import MP


class PreferenceManager(models.Manager):
    """
    Wraps mercadopago in a very simple interface that creates and manages
    django objects.
    """
    mp = None

    def connect(self):
        if not self.mp:
            self.mp = MP(
                settings.MERCADOPAGO_CLIENT_ID,
                settings.MERCADOPAGO_CLIENT_SECRET,
            )

    def create(self, title, price, reference):
        # TODO: validate that reference is unused
        self.connect()
        preference_request = {
            'items': [
                {
                    'title': title,
                    'quantity': 1,
                    'currency_id': 'ARS',
                    # In case we get something like Decimal:
                    'unit_price': float(price),
                }
            ],
            'external_reference': reference
        }

        preference_result = self.mp.create_preference(preference_request)

        preference = Preference(
            mp_id=preference_result['response']['id'],
            payment_url=preference_result['response']['init_point'],
            sandbox_url=preference_result['response']['sandbox_init_point'],
            # TODO: Make prefix configurable?
            reference='django_mercadopago_{}'.format(reference),
        )

        preference.save()
        return preference


class Preference(models.Model):
    """
    An MP payment preference.
    Price and other data is send to MP and not stored locally - it's assumed
    it's part of the model that relates to this one.
    """

    # Doc says it's a UUID. It's not.
    mp_id = models.CharField(max_length=46)

    payment_url = models.URLField()
    sandbox_url = models.URLField()
    reference = models.TextField(unique=True)

    objects = PreferenceManager()

    def __str__(self):
        return self.mp_id


class Payment(models.Model):
    """
    A payment received, related to a preference.
    """

    mp_id = models.IntegerField()

    preference = models.ForeignKey(
        Preference,
        related_name='payments',
    )
    status = models.CharField(max_length=16)
    status_detail = models.CharField(max_length=16)

    created = models.DateTimeField()

    def __str__(self):
        return self.mp_id
