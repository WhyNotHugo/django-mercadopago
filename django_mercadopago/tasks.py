from celery import shared_task

from django_mercadopago import models


@shared_task
def process_notification(notification_id):
    notification = models.Notification.objects.get(pk=notification_id)
    notification.process()
