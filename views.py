from django.http import HttpResponse

from .models import Notification


def create_notification(request):
    topic = request.GET.get('topic', None)
    resource_id = request.GET.get('id', None)

    if topic is None:
        return HttpResponse(
            '<h1>400 Bad Request.</h1>Missing parameter topic',
            status=400
        )
    if resource_id is None:
        return HttpResponse(
            '<h1>400 Bad Request.</h1>Missing parameter id',
            status=400
        )

    notification = Notification(resource_id=resource_id)

    if topic == 'merchant_order':
        notification.topic = Notification.TOPIC_ORDER
    elif topic == 'payment':
        notification.topic = Notification.TOPIC_PAYMENT
    else:
        return HttpResponse('invalid topic', status=400)

    notification.save()
    return HttpResponse("<h1>201 Created</h1>", status=201)
