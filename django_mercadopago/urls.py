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
        views.PostPaymentView.as_view(),
        name='post_payment',
    ),
]
