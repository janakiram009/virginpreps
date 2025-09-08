from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files for development
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

print("debugging:This is development settings file")
