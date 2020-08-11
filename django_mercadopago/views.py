import json
import logging

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from . import forms
from . import signals
from .models import Notification
from .models import Preference

logger = logging.getLogger(__name__)


def _create_notification(reference, topic, resource_id):
    try:
        preference = Preference.objects.get(reference=reference)
    except Preference.DoesNotExist:
        raise Http404("Invalid slug or reference.")

    notification, created = Notification.objects.update_or_create(
        topic=topic,
        resource_id=resource_id,
        owner=preference.owner,
        preference=preference,
        defaults={"status": Notification.STATUS_PENDING},
    )

    if settings.MERCADOPAGO["autoprocess"]:
        notification.process()
    signals.notification_received.send(sender=notification)

    return notification, created


class CSRFExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NotificationView(CSRFExemptMixin, View):
    def process(self, request, reference, form):
        if not form.is_valid():
            errors = form.errors.as_json()
            logger.warning(
                "Received an invalid notification: %r, %r",
                request.GET,
                errors,
                extra={"stack": True},
            )
            return HttpResponse(errors, status=400, content_type="application/json",)

        notification, created = _create_notification(
            reference,
            topic=form.TOPICS[form.cleaned_data["topic"]],
            resource_id=form.cleaned_data["id"],
        )

        return JsonResponse({"created": created}, status=201 if created else 200,)

    def get(self, request, reference):
        form = forms.NotificationForm(request.GET)
        return self.process(request, reference, form)

    def post(self, request, reference):
        # The format of notifications when getting a POST differs from the
        # format when getting a GET It can:
        #
        # * Have a JSON with the topic and id in different formats (type and
        #   data.id respectively)
        # * Have both in the QueryString
        data = json.loads(request.body)
        logger.info("Got POST notification: %s", data)
        form = forms.NotificationForm(
            {
                "topic": data.get("type", data.get("topic")),
                "id": data.get("data", {}).get("id", request.GET.get("id")),
            }
        )
        return self.process(request, reference, form)


class PaymentSuccessView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info("Reached payment success view with data: %r", request.GET)
        notification, created = _create_notification(
            reference,
            topic=Notification.TOPIC_PAYMENT,
            resource_id=request.GET.get("collection_id"),
        )

        return redirect(settings.MERCADOPAGO["success_url"], pk=notification.pk,)


class PaymentFailedView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info("Reached payment failure view with data: %r", request.GET)
        preference = Preference.objects.get(reference=reference)

        return redirect(settings.MERCADOPAGO["failure_url"], pk=preference.pk,)


class PaymentPendingView(CSRFExemptMixin, View):
    def get(self, request, reference):
        logger.info("Reached payment pending view with data: %r", request.GET)
        preference = Preference.objects.get(reference=reference)

        return redirect(settings.MERCADOPAGO["pending_url"], pk=preference.pk,)
