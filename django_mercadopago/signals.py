from django.dispatch import Signal


payment_received = Signal(
    providing_args=['payment']
)

notification_received = Signal()
