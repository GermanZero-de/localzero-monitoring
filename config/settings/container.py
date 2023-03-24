import platform
from .base import *

# overwrite locations so we can mount them into the container
DATABASES["default"]["NAME"] = Path("/") / "db" / "db.sqlite3"
STATIC_ROOT = "/static/"
MEDIA_ROOT = "/images/"
