import os

import pytest
from django.core.management import call_command

from config.settings.base import BASE_DIR

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            os.path.join(BASE_DIR, "e2e_tests", "database", "test_database.json"),
        )
