import platform
from .base import *

# overwrite locations so we can mount them into the container
DATABASES["default"]["NAME"] = Path("/") / "db" / "db.sqlite3"
STATIC_ROOT = "/static/"
MEDIA_ROOT = "/images/"

# pass in config parameters from docker compose environment:
SECRET_KEY = get_env("DJANGO_SECRET_KEY")
CSRF_TRUSTED_ORIGINS = get_env("DJANGO_CSRF_TRUSTED_ORIGINS").split(",")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env("DJANGO_DEBUG") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
