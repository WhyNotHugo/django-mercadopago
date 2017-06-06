import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import signals
from .models import Account, Notification

logger = logging.getLogger(__name__)


# Maybe use a form for this? :D

@csrf_exempt
def create_notification(request, slug):
    topic = request.GET.get('topic', None)
    resource_id = request.GET.get('id', None)

    if topic is None:
        return HttpResponse(
            '<h1>400 Bad Request.</h1>'
            'Missing parameter topic',
            status=400
        )
    if resource_id is None:
        return HttpResponse(
            '<h1>400 Bad Request.</h1>'
            'Missing parameter id',
            status=400
        )

    if topic == 'merchant_order':
        topic = Notification.TOPIC_ORDER
    elif topic == 'payment':
        topic = Notification.TOPIC_PAYMENT
    else:
        return HttpResponse('invalid topic', status=400)

    try:
        owner = Account.objects.get(slug=slug)
    except Account.DoesNotExist:
        return HttpResponse('Unknown account/slug', status=400)

    notification, created = Notification.objects.get_or_create(
        topic=topic,
        resource_id=resource_id,
        owner=owner,
    )

    if not created:
        notification.status = Notification.STATUS_PROCESSED
        notification.save()

    if settings.MERCADOPAGO_AUTOPROCESS:
        notification.process()

    signals.notification_received.send(
        sender=notification,
    )

    return HttpResponse('<h1>200 OK</h1>', status=201)


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
