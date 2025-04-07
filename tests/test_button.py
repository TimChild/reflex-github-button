import logging
import os
from pathlib import Path
from typing import Iterator

import pytest
from playwright.sync_api import Page, expect
from reflex.testing import AppHarness

PAGE_LOAD_TIMEOUT = 10000 if not os.getenv("CI") else 30000
INTERACTION_TIMEOUT = 2000 if not os.getenv("CI") else 20000


@pytest.fixture(scope="session")
def demo_app():
    app_root = Path(__file__).parent.parent / "github_button_demo"
    with AppHarness.create(root=app_root) as harness:
        yield harness


@pytest.fixture(scope="function")
def page(
    request: pytest.FixtureRequest, demo_app: AppHarness, page: Page
) -> Iterator[Page]:
    """Load the demo app main page."""
    page.set_default_timeout(PAGE_LOAD_TIMEOUT)
    assert demo_app.frontend_url is not None
    page.goto(demo_app.frontend_url)
    page.set_default_timeout(INTERACTION_TIMEOUT)
    yield page
    if request.session.testsfailed:
        logging.error("Test failed. Saving screenshot as playwright_test_error.png")
        page.screenshot(path="playwright_test_error.png")


def test_render(page: Page):
    """Check that the demo renders correctly.

    I.e. Check components are visible.
    """
    for button_type in [
        "follow",
        "sponsor",
        "watch",
        "star",
        "fork",
        "issue",
        "discuss",
        "download",
        "install this package",
        "use this template",
        "use this github action",
    ]:
        expect(
            page.get_by_test_id(f"gh-button-{button_type}").locator("span").nth(1)
        ).to_be_visible()
