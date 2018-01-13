from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^notifications/(?P<reference>.*)$',
        views.NotificationView.as_view(),
        name='notifications'
    ),
    url(
        r'^post_payment/(?P<reference>.*)$',
        views.PaymentSuccessView.as_view(),
        name='payment_success',
    ),
    url(
        r'^payment_failed/(?P<reference>.*)$',
        views.PaymentFailedView.as_view(),
        name='payment_failure',
    ),
    url(
        r'^payment_pending/(?P<reference>.*)$',
        views.PaymentPendingView.as_view(),
        name='payment_pending',
    ),
]
