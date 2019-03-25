from django.conf.urls import include, url


urlpatterns = [
    url('', include(('django_mercadopago.urls', 'django_mercadopago'), namespace='mp')),
]
