import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import forms, signals
from .models import Account, Notification

logger = logging.getLogger(__name__)


@csrf_exempt
def create_notification(request, slug):
    form = forms.NotificationForm(request.GET)
    if not form.is_valid():
        return HttpResponse(form.errors.as_json(), status=400)

    try:
        owner = Account.objects.get(slug=slug)
    except Account.DoesNotExist:
        return HttpResponse('Unknown account/slug', status=404)

    notification, created = Notification.objects.get_or_create(
        topic=form.TOPICS[form.cleaned_data['topic']],
        resource_id=form.cleaned_data['id'],
        owner=owner,
    )

    if not created:
        notification.status = Notification.STATUS_UNPROCESSED
        notification.save()

    if settings.MERCADOPAGO_AUTOPROCESS:
        notification.process()

    signals.notification_received.send(sender=notification)

    if created:
        return HttpResponse('<h1>201 Created</h1>', status=201)

    return HttpResponse('<h1>200 OK</h1>', status=200)


class PostPaymentView(View):

    def get(self, request, slug):
        collection_id = request.GET.get('collection_id')

        try:
            owner = Account.objects.get(slug=slug)
        except Account.DoesNotExist:
            return HttpResponse('Unknown account/slug', status=400)

        notification, created = Notification.objects.get_or_create(
            topic=Notification.TOPIC_PAYMENT,
            resource_id=collection_id,
            owner=owner,
        )

        if not created:
            notification.status = Notification.STATUS_WITH_UPDATES
            notification.save()

        if settings.MERCADOPAGO_AUTOPROCESS:
            notification.process()
        # TODO: Else add to some queue?

        return HttpResponseRedirect(reverse(
            settings.MERCADOPAGO_POST_PAYMENT_VIEW,
            args=(notification.pk,),
        ))

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
