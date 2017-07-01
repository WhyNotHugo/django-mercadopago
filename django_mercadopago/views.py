import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import forms, signals
from .models import Account, Notification

logger = logging.getLogger(__name__)


def _create_notification(slug, topic, resource_id):
    qs = Account.objects.filter(slug=slug)
    account = get_object_or_404(qs)

    notification, created = Notification.objects.get_or_create(
        topic=topic,
        resource_id=resource_id,
        owner=account,
    )

    if not created:
        notification.status = Notification.STATUS_UNPROCESSED
        notification.save()

    if settings.MERCADOPAGO_AUTOPROCESS:
        notification.process()
    signals.notification_received.send(sender=notification)

    return notification, created


class CSRFExemptMixin:

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NotificationView(CSRFExemptMixin, View):

    def get(self, request, slug):
        form = forms.NotificationForm(request.GET)
        if not form.is_valid():
            errors = form.errors.as_json()
            logger.warning('Received an invalid notification: %r', errors)
            return HttpResponse(errors, status=400)

        notification, created = _create_notification(
            slug,
            topic=form.TOPICS[form.cleaned_data['topic']],
            resource_id=form.cleaned_data['id'],
        )

        if created:
            return HttpResponse('<h1>201 Created</h1>', status=201)

        return HttpResponse('<h1>200 OK</h1>', status=200)


class PostPaymentView(CSRFExemptMixin, View):

    def get(self, request, slug):
        notification, created = _create_notification(
            slug,
            topic=Notification.TOPIC_PAYMENT,
            resource_id=request.GET.get('collection_id'),
        )

        return HttpResponseRedirect(reverse(
            settings.MERCADOPAGO_POST_PAYMENT_VIEW,
            args=(notification.pk,),
        ))
