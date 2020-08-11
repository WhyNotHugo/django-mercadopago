SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "django_mercadopago",
    "tests",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
ROOT_URLCONF = "tests.urls"

MERCADOPAGO = {
    "autoprocess": False,
    "base_host": "http://localhost:8001",
    "success_url": "mp_success",  # Inexistant
    "failure_url": "mp_failure",  # Inexistant
    "pending_url": "mp_pending",  # Inexistant
}
