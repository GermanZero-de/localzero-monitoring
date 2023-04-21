import pytest
from playwright.sync_api import Page, BrowserContext


@pytest.fixture
def page(context: BrowserContext) -> Page:
    # Generate base64 encoded user:password with `echo -n "user:password" | base64`
    context.set_extra_http_headers({"Authorization": "Basic a2VybnRlYW06cGFzc3dvcmQ="})
    return context.new_page()
