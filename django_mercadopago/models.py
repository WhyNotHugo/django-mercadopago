import logging

import requests
from django.conf import settings
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mercadopago import MP

from . import signals

logger = logging.getLogger(__name__)


class MercadoPagoServiceException(Exception):
    pass


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
        unique=True,
        help_text=_("This slug is used for this account's notification URL.")
    )
    app_id = models.CharField(
        _('client id'),
        max_length=16,
        help_text=_('The APP_ID given by MercadoPago.'),
    )
    secret_key = models.CharField(
        _('secret key'),
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

    def __repr__(self):
        return '<Account {}: {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    @property
    def service(self):
        return MercadoPagoService(self)


class PreferenceManager(models.Manager):
    """
    Wraps mercadopago in a very simple interface that creates and manages
    django objects.
    """

    def create(
        self,
        title,
        description,
        price,
        reference,
        account,
        quantity=1,
        category='services',
        extra_fields=None,
        host=settings.MERCADOPAGO['base_host'],
    ):
        """
        Creates a new preference and registers it in MercadoPago's API.

        :param str title: The title users will see in MercadoPago
        :param price: The price for this preference.
        :type price: float or Decimal
        :param str reference: A reference by which we'll later search for and
            identify this preference.
        :param Account account: The account for which this payment is to be
            created.
        :param quantity: The quantity for this preference.
        :type quantity: integer
        :param dict extra_fields: Extra infromation to be sent with the
            preference creation (including payer). See the documentation[1] for
            details on avaiable fields.
        :param str host: The host to prepend to notification and return URLs.
            This should be the host for the cannonical URL where this app is
            served.

        [1]: https://www.mercadopago.com.ar/developers/es/api-docs/basic-checkout/checkout-preferences/
        """  # noqa
        extra_fields = extra_fields or {}

        notification_url = host + reverse(
            'mp:notifications', args=(reference,)
        )
        success_url = host + reverse('mp:payment_success', args=(reference,))
        failure_url = host + reverse('mp:payment_failure', args=(reference,))
        pending_url = host + reverse('mp:payment_pending', args=(reference,))

        # TODO: validate that reference is unused
        preference_request = {
            'auto_return': 'all',
            'items': [
                {
                    'title': title,
                    'currency_id': 'ARS',
                    'description': description,
                    'category_id': category,
                    'quantity': quantity,
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
        preference_request.update(extra_fields)

        mercadopago_service = account.service
        pref_result = mercadopago_service.create_preference(preference_request)

        if pref_result['status'] >= 300:
            logger.warning('MercadoPago returned non-200', pref_result)
            raise MercadoPagoServiceException(
                'MercadoPago failed to create preference', pref_result
            )

        preference = Preference(
            title=title,
            price=price,
            quantity=quantity,
            mp_id=pref_result['response']['id'],
            payment_url=pref_result['response']['init_point'],
            sandbox_url=pref_result['response']['sandbox_init_point'],
            # TODO: Make prefix configurable?
            reference=reference,
            owner=account,
        )

        preference.save()
        return preference


class Preference(models.Model):
    """
    An MP payment preference.

    Related data is send to MP and not stored locally - it's assumed
    it's part of the model that relates to this one.
    """

    owner = models.ForeignKey(
        Account,
        verbose_name=_('owner'),
        related_name='preferences',
        on_delete=models.PROTECT,
    )

    title = models.CharField(
        _('title'),
        max_length=256,
    )
    price = models.DecimalField(
        _('price'),
        max_digits=15,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        _('quantity'),
        default=1,
    )
    # Doc says it's a UUID. It's not.
    mp_id = models.CharField(
        _('mercadopago id'),
        max_length=46,
        help_text=_('The id MercadoPago has assigned for this Preference')
    )

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
    paid = models.BooleanField(
        _('paid'),
        default=False,
        help_text=_('Indicates if the preference has been paid.'),
    )

    objects = PreferenceManager()

    @property
    def url(self):
        if self.owner.sandbox:
            return self.sandbox_url
        else:
            return self.payment_url

    def update(self, title=None, price=None, quantity=None):
        """
        Updates the upstream Preference with the supplied title and price.
        """
        if price:
            self.price = price
        if title:
            self.title = title
        if quantity:
            self.quantity = quantity

        service = self.owner.service
        service.update_preference(
            self.mp_id,
            {
                'items': [
                    {
                        'title': self.title,
                        'quantity': self.quantity,
                        'currency_id': 'ARS',
                        'unit_price': float(self.price),
                    }
                ]
            }
        )
        self.save()

    def poll_status(self):
        """
        Manually poll for the status of this preference.
        """
        service = self.owner.service
        response = requests.get(
            'https://api.mercadopago.com/v1/payments/search',
            params={
                'access_token': service.get_access_token(),
                'external_reference': self.reference,
            },
        )
        response.raise_for_status()
        response = response.json()

        if response['results']:
            logger.info('Polled for %s. Creating Payment', self.pk)
            return Payment.objects.create_or_update_from_raw_data(
                response['results'][-1]
            )
        else:
            logger.info('Polled for %s. No data', self.pk)

    def get_absolute_url(self):
        return self.url

    def __repr__(self):
        return '<Preference {}: mp_id: {}, paid: {}>'.format(
            self.id,
            self.mp_id,
            self.paid
        )

    def __str__(self):
        return self.mp_id


class PaymentManager(models.Manager):

    def create_or_update_from_raw_data(self, raw_data):
        # Older endpoints will use this formats, newer one won't.
        if 'collection' in raw_data:
            raw_data = raw_data['collection']

        preference = Preference.objects.filter(
            reference=raw_data['external_reference'],
        ).first()
        if not preference:
            logger.warning(
                "Got notification for a preference that's not ours."
            )
            return

        if 'date_approved' in raw_data:
            approved = raw_data['date_approved']
        else:
            approved = None

        payment_data = {
            'status': raw_data['status'],
            'status_detail': raw_data['status_detail'],
            'created': raw_data['date_created'],
            'approved': approved,
        }

        payment, created = Payment.objects.update_or_create(
            preference=preference,
            mp_id=raw_data['id'],
            defaults=payment_data,
        )

        if payment.status == 'approved' and \
           payment.status_detail == 'accredited':
            preference.paid = True
            preference.save()

            signals.payment_received.send(
                sender=Preference,
                payment=payment,
            )

        return payment


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
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _('status'),
        max_length=16,
    )
    status_detail = models.CharField(
        _('status detail'),
        max_length=32,
    )

    created = models.DateTimeField(
        _('created'),
    )
    approved = models.DateTimeField(
        _('approved'),
        null=True,
    )

    notification = models.OneToOneField(
        'Notification',
        verbose_name=_('notification'),
        related_name='payment',
        help_text=_('The notification that informed us of this payment.'),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def __repr__(self):
        return '<Payment {}: mp_id: {}>'.format(
            self.id,
            self.mp_id,
        )

    def __str__(self):
        return str(self.mp_id)

    objects = PaymentManager()


class Notification(models.Model):
    """
    A notification received from MercadoPago.
    """

    TOPIC_ORDER = 'o'
    TOPIC_PAYMENT = 'p'

    STATUS_PENDING = 'unp'
    STATUS_PROCESSED = 'pro'
    STATUS_IGNORED = 'ign'

    STATUS_OK = 'ok'
    STATUS_404 = '404'
    STATUS_ERROR = 'err'

    owner = models.ForeignKey(
        Account,
        verbose_name=_('owner'),
        related_name='notifications',
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        _('status'),
        max_length=3,
        choices=(
            (STATUS_PENDING, _('Pending')),
            (STATUS_PROCESSED, _('Processed')),
            (STATUS_IGNORED, _('Ignored')),
            (STATUS_OK, _('Okay')),
            (STATUS_404, _('Error 404')),
            (STATUS_ERROR, _('Error')),
        ),
        default=STATUS_PENDING,
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
    preference = models.ForeignKey(
        Preference,
        verbose_name=_('preference'),
        related_name='notifications',
        null=True,
        on_delete=models.PROTECT,
    )

    @property
    def processed(self):
        return self.status == Notification.STATUS_PROCESSED

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
            self.status = Notification.STATUS_IGNORED
            self.save()
            return

        mercadopago_service = self.owner.service
        raw_data = mercadopago_service.get_payment_info(self.resource_id)

        if raw_data['status'] != 200:
            logger.warning(
                'Got status code %d for notification %d.',
                raw_data['status'],
                self.id
            )
            if raw_data['status'] == 404:
                self.status = Notification.STATUS_404
            else:
                self.status = Notification.STATUS_ERROR

            self.save()
            return

        response = raw_data['response']

        payment = Payment.objects.create_or_update_from_raw_data(response)
        if payment:
            payment.notification = self
            payment.save()

        self.status = Notification.STATUS_PROCESSED
        self.save()

        return payment

    def __repr__(self):
        return '<Notification {}: {} {}, owner: {}>'.format(
            self.id,
            self.get_topic_display(),
            self.resource_id,
            self.owner_id,
        )

    def __str__(self):
        return '{} {}'.format(self.get_topic_display(), self.resource_id)
