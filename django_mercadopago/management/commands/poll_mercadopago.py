from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from django_mercadopago.models import Preference


class Command(BaseCommand):
    help = _(
        'Poll MercadoPago to fetch and possible updates to unpaid Preferences'
    )

    def handle(self, *args, **options):
        for preference in Preference.objects.filter(
            paid=False,
        ).order_by(
            '-pk'
        ):
            preference.poll_status()
