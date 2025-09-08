from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Static files for development
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
