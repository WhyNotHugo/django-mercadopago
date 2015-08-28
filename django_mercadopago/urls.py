from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^notifications$', views.create_notification),
]
