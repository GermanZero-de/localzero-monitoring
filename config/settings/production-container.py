import platform
from .production import *
from pathlib import Path

# overwrite db location so we can mount it into the container
DATABASES["default"]["NAME"] = Path("/") / "db" / "db.sqlite3"
