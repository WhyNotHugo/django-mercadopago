from django.conf.urls import include, url

from django_mercadopago import urls as mp_urls


urlpatterns = [
    url(r'^', include((mp_urls, 'mp'), 'mp')),
]
