import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Notification, Account

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

    owner = Account.objects.get(slug=slug)
    notification, created = Notification.objects.get_or_create(
        topic=topic,
        resource_id=resource_id,
        owner=owner,
    )

    if not created:
        notification.processed = False
        notification.save()

    if not settings.MERCADOPAGO_ASYNC:
        notification.process()
    # TODO: Else add to some queue?

    return HttpResponse("<h1>200 OK</h1>", status=201)
