SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django_mercadopago',
    'tests',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = 'django_mercadopago.urls'

MERCADOPAGO_BASE_HOST = 'http://localhost:8001'
MERCADOPAGO_AUTOPROCESS = False
