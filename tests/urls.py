from django.conf.urls import include
from django.urls import re_path

from django_mercadopago import urls as mp_urls


urlpatterns = [
    re_path(r"^", include((mp_urls, "mp"), "mp")),
]
