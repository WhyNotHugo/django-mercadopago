from django import forms

from django_mercadopago import models


class NotificationForm(forms.Form):
    TOPICS = {
        'merchant_order': models.Notification.TOPIC_ORDER,
        'payment': models.Notification.TOPIC_PAYMENT,
    }

    id = forms.CharField()
    topic = forms.ChoiceField(choices=TOPICS.items())
