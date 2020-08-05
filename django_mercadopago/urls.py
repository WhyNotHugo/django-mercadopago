from django.urls import path

from . import views

urlpatterns = [
    path(
        "notifications/<reference>",
        views.NotificationView.as_view(),
        name="notifications",
    ),
    path(
        "post_payment/<reference>",
        views.PaymentSuccessView.as_view(),
        name="payment_success",
    ),
    path(
        "payment_failed/<reference>",
        views.PaymentFailedView.as_view(),
        name="payment_failure",
    ),
    path(
        "payment_pending/<reference>",
        views.PaymentPendingView.as_view(),
        name="payment_pending",
    ),
]
