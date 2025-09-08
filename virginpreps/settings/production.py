from .base import *

DEBUG = False
ALLOWED_HOSTS = ["virginpreps.com", "www.virginpreps.com", "210.79.129.39"]

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

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Static files for production
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
