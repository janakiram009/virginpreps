from .base import *

DEBUG = False
ALLOWED_HOSTS = ["virginpreps.com", "www.virginpreps.com", "srinivasasnature.com", "www.srinivasasnature.com"]

# Production-specific settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Static files for production
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

print("This is production settings file")
