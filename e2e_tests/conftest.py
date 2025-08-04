import os

import pytest
from django.core.management import call_command
from playwright.sync_api import Page, BrowserContext

from config.settings.base import BASE_DIR


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # ignore complaints that our self-signed localhost cert isn't trusted by playwright
    return {**browser_context_args, "ignore_https_errors": True}


@pytest.fixture(scope="session")
def base_url():
    return "https://localhost"
