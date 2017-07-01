from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^notifications/(?P<key>.*)$',
        views.NotificationView.as_view(),
        name='notifications'
    ),
    url(
        r'^post_payment/(?P<key>.*)$',
        views.PostPaymentView.as_view(),
        name='post_payment',
    ),
]
