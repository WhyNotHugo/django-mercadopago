import json
import logging

from django.conf import settings
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import forms, signals
from .models import Account, Notification, Preference

logger = logging.getLogger(__name__)


def _create_notification(key, topic, resource_id):
    try:
        account = Account.objects.get(slug=key)
    except Account.DoesNotExist:
        try:
            preference = Preference.objects.get(reference=key)
        except Preference.DoesNotExist:
            raise Http404('Invalid slug or reference.')
        else:
            account = preference.owner
    else:
        preference = None

    notification, created = Notification.objects.update_or_create(
        topic=topic,
        resource_id=resource_id,
        owner=account,
        preference=preference,
        defaults={
            'status': Notification.STATUS_PENDING,
        },
    )

    if settings.MERCADOPAGO_AUTOPROCESS:
        notification.process()
    signals.notification_received.send(sender=notification)

    return notification, created


class CSRFExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NotificationView(CSRFExemptMixin, View):
    def process(self, request, key, form):
        if not form.is_valid():
            errors = form.errors.as_json()
            logger.warning(
                'Received an invalid notification: %r, %r',
                request.GET,
                errors,
            )
            return HttpResponse(
                errors,
                status=400,
                content_type='application/json',
            )

        notification, created = _create_notification(
            key,
            topic=form.TOPICS[form.cleaned_data['topic']],
            resource_id=form.cleaned_data['id'],
        )

        return JsonResponse(
            {'created': created},
            status=201 if created else 200,
        )

    def get(self, request, key):
        form = forms.NotificationForm(request.GET)
        return self.process(request, key, form)

    def post(self, request, key):
        # The format of notifications when getting a POST differs from the
        # format when getting a GET, so map these:
        data = json.loads(request.body)
        logger.info('Got POST notification: %s', data)
        form = forms.NotificationForm(
            {
                'topic': data.get('type'),
                'id': data.get('data', {}).get('id'),
            }
        )
        return self.process(request, key, form)


class PostPaymentView(CSRFExemptMixin, View):

    def get(self, request, key):
        logger.info('Reached post-payment view with data: %r', request.GET)
        notification, created = _create_notification(
            key,
            topic=Notification.TOPIC_PAYMENT,
            resource_id=request.GET.get('collection_id'),
        )

        return HttpResponseRedirect(reverse(
            settings.MERCADOPAGO_POST_PAYMENT_VIEW,
            args=(notification.pk,),
        ))
