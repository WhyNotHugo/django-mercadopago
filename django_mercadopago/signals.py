import logging

from django.conf import settings
from django.dispatch import Signal


payment_received = Signal(providing_args=['payment'])
notification_received = Signal()

logger = logging.getLogger(__name__)


def process_new_notification(sender, instance, **kwargs):
    # XXX: what if a user is being redireected and we expect the status to be
    # updated?

    if settings.MERCADOPAGO['autoprocess'] == 'SYNC':
        instance.process()
    elif settings.MERCADOPAGO['autoprocess'] == 'ASYNC':
        from django_mercadopago import tasks
        tasks.process_notification.delay(instance.pk)
    else:
        logger.debug('Notification not auto-processed.')
