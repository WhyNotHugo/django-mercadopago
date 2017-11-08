SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django_mercadopago',
    'tests',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
