from django.conf.urls import include, url


urlpatterns = [
    url(r'^mercadopago/', include(('django_mercadopago.urls', 'django_mercadopago'), namespace='mp')),
]
