import logging

from django.conf import settings
from django.db import models
from django.db import transaction
from django.utils.functional import LazyObject
from mercadopago import MP

logger = logging.getLogger(__name__)


class MercadoPagoService(LazyObject):
    """
    MercadoPago service (the same one from the SDK), lazy-initialized on first
    access.
    """

    def _setup(self):
        mp = MP(
                settings.MERCADOPAGO_CLIENT_ID,
                settings.MERCADOPAGO_CLIENT_SECRET,
        )
        mp.sandbox_mode(settings.MERCADOPAGO_SANDBOX)
        self._wrapped = mp


mercadopago_service = MercadoPagoService()


class PreferenceManager(models.Manager):
    """
    Wraps mercadopago in a very simple interface that creates and manages
    django objects.
    """

    def create(self, title, price, reference, success_url, pending_url=None,
               failure_url=None):
        """
        Creates a new preference and registers it in MercadoPago's API.

        If pending_url or failure_url are None, success_url will be used for
        these.
        """
        pending_url = pending_url or success_url
        failure_url = failure_url or success_url

        reference = 'django_mercadopago_{}'.format(reference),

        # TODO: validate that reference is unused
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
            'external_reference': reference,
            'back_urls': {
                'success': success_url,
                'pending': pending_url,
                'failure': failure_url,
            },
        }

        pref_result = mercadopago_service.create_preference(preference_request)

        if pref_result['status'] >= 300:
            logger.warning('MercadoPago returned non-200', pref_result)
            raise Exception(
                'MercadoPago failed to create preference', pref_result
            )

        preference = Preference(
            mp_id=pref_result['response']['id'],
            payment_url=pref_result['response']['init_point'],
            sandbox_url=pref_result['response']['sandbox_init_point'],
            # TODO: Make prefix configurable?
            reference=reference,
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

    @property
    def url(self):
        if settings.MERCADOPAGO_SANDBOX:
            return self.sandbox_url
        else:
            return self.payment_url

    def __str__(self):
        return self.mp_id


class Payment(models.Model):
    """
    A payment received, related to a preference.
    """

    mp_id = models.IntegerField(unique=True)

    preference = models.ForeignKey(
        Preference,
        related_name='payments',
    )
    status = models.CharField(max_length=16)
    status_detail = models.CharField(max_length=16)

    created = models.DateTimeField()
    approved = models.DateTimeField()

    def __str__(self):
        return str(self.mp_id)


class Notification(models.Model):
    """
    A notification received from MercadoPago.
    """

    TOPIC_ORDER = 'o'
    TOPIC_PAYMENT = 'p'

    topic = models.CharField(
        max_length=1,
        choices=(
            (TOPIC_ORDER, 'Merchant Order',),
            (TOPIC_PAYMENT, 'Payment',),
        ),
    )
    resource_id = models.CharField(max_length=46)
    # TODO: We need some locking mechanism to deal with concurrency here:
    processed = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('topic', 'resource_id',),
        )

    @transaction.atomic
    def process(self):
        """
        Processes the notification, and returns the generated payment, if
        applicable.
        """
        raw_data = mercadopago_service.get_payment_info(self.resource_id)
        if raw_data['status'] != 200:
            logger.info('Got non-200 for notification {}.', self.id)
            return None

        reference = raw_data['response']['collection']['external_reference']

        try:
            preference = Preference.objects.get(reference=reference)
        except Preference.DoesNotExist:
            logger.info(
                "Got notification for a preference that's not ours. Ignoring"
            )
            return

        # XXX TODO: The payment might exist. Deal with it.

        payment = Payment(
            mp_id=raw_data['response']['collection']['id'],
            preference=preference,
            status=raw_data['response']['collection']['status'],
            status_detail=raw_data['response']['collection']['status_detail'],
            created=raw_data['response']['collection']['date_created'],
            approved=raw_data['response']['collection']['date_approved'],
        )
        self.processed = True

        payment.save()
        self.save()
        return payment

    def __str__(self):
        return '{} {}'.format(self.topic, self.resource_id)
