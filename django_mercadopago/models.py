import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext as _
from mercadopago import MP

logger = logging.getLogger(__name__)


class MercadoPagoService(MP):
    """
    MercadoPago service (the same one from the SDK), lazy-initialized on first
    access.
    """

    def __init__(self, account):
        super().__init__(account.app_id, account.secret_key)
        self.sandbox_mode(account.sandbox)


class Account(models.Model):
    """
    A mercadopago account, aka "application".
    """
    name = models.CharField(
        _('name'),
        max_length=32,
        help_text=_('A friendly name to recognize this account.'),
    )
    slug = models.SlugField(
        _('slug'),
        help_text=_("This slug is used for this account's notification URL.")
    )
    app_id = models.CharField(
        _('client id'),
        max_length=16,
        help_text=_('The APP_ID given by MercadoPago.'),
    )
    secret_key = models.CharField(
        _('client id'),
        max_length=32,
        help_text=_('The SECRET_KEY given by MercadoPago.'),
    )
    sandbox = models.BooleanField(
        _('sandbox'),
        default=True,
        help_text=_(
            'Indicates if this account uses the sandbox mode, '
            'indicated for testing rather than real transactions.'
        ),
    )

    def __str__(self):
        return self.name

    def get_service(self):
        return MercadoPagoService(self)


class PreferenceManager(models.Manager):
    """
    Wraps mercadopago in a very simple interface that creates and manages
    django objects.
    """

    def create(self, title, price, reference, account, success_url,
               pending_url=None, failure_url=None):
        """
        Creates a new preference and registers it in MercadoPago's API.

        If pending_url or failure_url are None, success_url will be used for
        these.
        """
        pending_url = pending_url or success_url
        failure_url = failure_url or success_url

        notification_url = settings.MERCADOPAGO_BASE_HOST + \
            reverse('mp:notifications', args=(account.slug,))
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
            'notification_url': notification_url,
        }

        mercadopago_service = account.get_service()
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

    payment_url = models.URLField(
        _('payment url'),
    )
    sandbox_url = models.URLField(
        _('sandbox url'),
    )
    reference = models.CharField(
        _('reference'),
        max_length=128,
        unique=True,
    )

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

    mp_id = models.IntegerField(
        _('mp id'),
        unique=True,
    )

    preference = models.ForeignKey(
        Preference,
        verbose_name=_('preference'),
        related_name='payments',
    )
    status = models.CharField(
        _('status'),
        max_length=16,
    )
    status_detail = models.CharField(
        _('status detail'),
        max_length=16,
    )

    created = models.DateTimeField(
        _('created'),
    )
    approved = models.DateTimeField(
        _('approved'),
    )

    notification = models.OneToOneField(
        'Notification',
        verbose_name=_('notification'),
        related_name='payment',
        help_text=_('The notification that informed us of this payment.'),
    )

    def __str__(self):
        return str(self.mp_id)


class Notification(models.Model):
    """
    A notification received from MercadoPago.
    """

    TOPIC_ORDER = 'o'
    TOPIC_PAYMENT = 'p'

    STATUS_UNPROCESSED = 'unp'
    STATUS_OK = 'ok'
    STATUS_404 = '404'
    # More statuses will probably appear here...

    owner = models.ForeignKey(
        Account,
        verbose_name=_('owner'),
        related_name='notifications',
    )
    status = models.CharField(
        _('status'),
        max_length=3,
        choices=(
            (STATUS_UNPROCESSED, _('Unprocessed')),
            (STATUS_OK, _('Okay')),
            (STATUS_404, _('Error 404')),
        ),
        default=STATUS_UNPROCESSED,
    )
    topic = models.CharField(
        max_length=1,
        choices=(
            (TOPIC_ORDER, 'Merchant Order',),
            (TOPIC_PAYMENT, 'Payment',),
        ),
    )
    resource_id = models.CharField(
        _('resource_id'),
        max_length=46,
    )
    processed = models.BooleanField(
        _('processed'),
        default=False,
    )

    last_update = models.DateTimeField(
        _('last_update'),
        auto_now=True,
    )

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
        if self.topic == Notification.TOPIC_ORDER:
            logger.info("We don't process order notifications yet")
            self.processed = True
            self.save()
            return

        mercadopago_service = self.owner.get_service()
        raw_data = mercadopago_service.get_payment_info(self.resource_id)

        if raw_data['status'] != 200:
            logger.warning(
                'Got status code %d for notification %d.',
                raw_data['status'],
                self.id
            )
            self.status = Notification.STATUS_404
            self.processed = True
            return

        reference = raw_data['response']['collection']['external_reference']

        try:
            preference = Preference.objects.get(reference=reference)
        except Preference.DoesNotExist:
            logger.info(
                "Got notification for a preference that's not ours. Ignoring"
            )
            return

        mp_id = raw_data['response']['collection']['id']
        try:
            payment = Payment.objects.get(mp_id=mp_id)
        except Payment.DoesNotExist:
            payment = Payment(mp_id=mp_id)

        payment.preference = preference
        payment.status = raw_data['response']['collection']['status']
        payment.status_detail = \
            raw_data['response']['collection']['status_detail']
        payment.created = raw_data['response']['collection']['date_created']
        payment.approved = raw_data['response']['collection']['date_approved']
        payment.notification = self
        self.processed = True

        payment.save()
        self.save()
        return payment

    def __str__(self):
        return '{} {}'.format(self.get_topic_display(), self.resource_id)
