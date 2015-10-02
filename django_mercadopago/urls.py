from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^notifications/(?P<slug>.*)$',
        views.create_notification,
        name='notifications'
    ),
]
