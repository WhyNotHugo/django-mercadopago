from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^notifications/(?P<pk>.*)$',
        views.create_notification,
        name='notifications'
    ),
]
