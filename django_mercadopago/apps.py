from django.apps import AppConfig


class MercadoPagoConfig(AppConfig):
    name = 'django_mercadopago'
    label = 'mp'
    verbose_name = 'MercadoPago'

    def ready(self):
        from django_mercadopago import models, signals

        signals.notification_received.connect(
            signals.process_new_notification,
            sender=models.Notification,
        )
