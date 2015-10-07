from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^notifications/(?P<slug>.*)$',
        views.create_notification,
        name='notifications'
    ),
    url(
        r'^post_payment/(?P<slug>.*)$',
        views.PostPaymentView.as_view(),
        name='post_payment',
    ),
]
